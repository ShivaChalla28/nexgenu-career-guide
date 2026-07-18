import os
import glob

# We are searching for relative API calls OR the Render URLs, and replacing them with localhost
search_texts = [
    "fetch('/api/", 
    "fetch(`/api/",
    "fetch('https://nexgenu-career-guide.onrender.com/api/",
    "fetch(`https://nexgenu-career-guide.onrender.com/api/"
]
replace_text_single = "fetch('http://localhost:8000/api/"
replace_text_template = "fetch(`http://localhost:8000/api/"

frontend_dir = os.path.join("frontend", "src")

files_changed = 0
for ext in ("**/*.tsx", "**/*.ts"):
    for filepath in glob.glob(os.path.join(frontend_dir, ext), recursive=True):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        original_content = content
        
        # Replace relative paths
        content = content.replace("fetch('/api/", replace_text_single)
        content = content.replace("fetch(`/api/", replace_text_template)
        
        # Replace Render absolute paths
        content = content.replace("fetch('https://nexgenu-career-guide.onrender.com/api/", replace_text_single)
        content = content.replace("fetch(`https://nexgenu-career-guide.onrender.com/api/", replace_text_template)
        
        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Restored to localhost:8000 -> {filepath}")
            files_changed += 1

print(f"\nDone! Successfully restored {files_changed} files back to localhost:8000.")
