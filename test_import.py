import traceback
import sys

print("Python path:", sys.path)

try:
    import app.api.v1.payments
    print("Payments module imported successfully")
except Exception as e:
    print(f"Failed to import payments module: {e}")
    traceback.print_exc()

try:
    import app.main
    print("Main module imported successfully")
except Exception as e:
    print(f"Failed to import main module: {e}")
    traceback.print_exc()
