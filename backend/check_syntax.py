import sys
import traceback
try:
    import main
    from routers import admin
    print("Syntax check passed!")
except Exception as e:
    print("Error during import:")
    traceback.print_exc()
