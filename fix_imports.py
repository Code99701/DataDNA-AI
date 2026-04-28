import os

BASE_DIR = r"d:\google solutions\Google-Solutions-2026-Project\backend_final\app"

files = [
    os.path.join(BASE_DIR, "api", "routes", "auth.py"),
    os.path.join(BASE_DIR, "api", "routes", "admin.py"),
    os.path.join(BASE_DIR, "api", "dependencies.py"),
    os.path.join(BASE_DIR, "services", "auth_service.py")
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        content = content.replace("app.db.database", "app.database.database")
        content = content.replace("app.db.auth_models", "app.models.auth_models")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print("Imports fixed!")
