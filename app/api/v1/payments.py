from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from typing import Optional
import stripe
from app.config.database import get_db
from app.config.settings import settings
from app.models.borrowing import Borrowing, BorrowingStatus
from app.schemas.payments import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/create-checkout-session", response_model=PaymentResponse)
async def create_checkout_session(
    payment: PaymentCreate,
    db: AsyncSession = Depends(get_db)
):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Fetch borrowing
    query = select(Borrowing).where(Borrowing.id == payment.borrowing_id)
    result = await db.execute(query)
    borrowing = result.scalar_one_or_none()

    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing record not found")

    if borrowing.fine_paid:
        raise HTTPException(status_code=400, detail="Fine already paid")
        
    if borrowing.fine_amount <= 0:
        raise HTTPException(status_code=400, detail="No fine to pay")

    try:
        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': settings.STRIPE_CURRENCY,
                        'product_data': {
                            'name': 'Library Overdue Fine',
                            'description': f'Fine for borrowing ID: {borrowing.id}',
                        },
                        # Stripe amount is in cents
                        'unit_amount': int(borrowing.fine_amount * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8000/cancel',
            metadata={
                'borrowing_id': payment.borrowing_id
            }
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
    db: AsyncSession = Depends(get_db)
):
    payload = await request.body()
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Check if payment was successful
        if session.payment_status == 'paid':
            borrowing_id_str = session.get('metadata', {}).get('borrowing_id')
            
            if borrowing_id_str:
                borrowing_id = int(borrowing_id_str)
                
                # Fetch and update borrowing record
                query = select(Borrowing).where(Borrowing.id == borrowing_id)
                result = await db.execute(query)
                borrowing = result.scalar_one_or_none()
                
                if borrowing:
                    borrowing.fine_paid = True
                    await db.commit()
                    
    return {"status": "success"}
