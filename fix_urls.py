import os
import glob

search_text = "http://localhost:8000"
replace_text = "https://nexgenu-career-guide.onrender.com"
frontend_dir = os.path.join("frontend", "src")

print(f"Searching for '{search_text}' in {frontend_dir}...")

files_changed = 0
# Find all .tsx and .ts files
for ext in ("**/*.tsx", "**/*.ts"):
    for filepath in glob.glob(os.path.join(frontend_dir, ext), recursive=True):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if search_text in content:
            new_content = content.replace(search_text, replace_text)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Updated {filepath}")
            files_changed += 1

print(f"\nDone! Successfully updated API URLs in {files_changed} files.")
