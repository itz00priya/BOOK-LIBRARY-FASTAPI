import sys
with open('.env', 'rb') as f:
    content = f.read()
content = content.replace(b'\r', b'')
with open('.env', 'wb') as f:
    f.write(content)
print("Carriage returns stripped from .env")
