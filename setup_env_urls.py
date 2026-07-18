import os
import glob
import re

frontend_dir = os.path.join("frontend", "src")

# We want to replace fetch('/api/...') with fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/...`)
# We also want to replace fetch(`...`) if they are template literals.

files_changed = 0
for ext in ("**/*.tsx", "**/*.ts"):
    for filepath in glob.glob(os.path.join(frontend_dir, ext), recursive=True):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Strip hardcoded Render URLs first just in case
        content = content.replace("https://nexgenu-career-guide.onrender.com", "")
        content = content.replace("http://localhost:8000", "")
        
        # Replace fetch('/api/...
        content = re.sub(r"fetch\('/api/([^']+)'", r"fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/\1`", content)
        
        # Replace fetch(`/api/...
        content = re.sub(r"fetch\(`/api/([^`]+)`", r"fetch(`${process.env.NEXT_PUBLIC_API_URL || ''}/api/\1`", content)
        
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Configured Dynamic API URL -> {filepath}")
            files_changed += 1

print(f"\nDone! Successfully updated {files_changed} files to use NEXT_PUBLIC_API_URL.")
