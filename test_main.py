import sys
import traceback

print("Starting import test")
try:
    import app.main
    print("Successfully imported app.main")
except Exception as e:
    print("Error during import:")
    traceback.print_exc()
