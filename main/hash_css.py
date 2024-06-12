import hashlib
import os

def generate_hash(file_path):
    with open(file_path, 'rb') as f:
        file_content = f.read()
    return hashlib.md5(file_content).hexdigest()

def rename_css_file(file_path):
    file_dir, file_name = os.path.split(file_path)
    name, ext = os.path.splitext(file_name)
    file_hash = generate_hash(file_path)
    new_file_name = f"{name}.{file_hash}{ext}"
    new_file_path = os.path.join(file_dir, new_file_name)
    os.rename(file_path, new_file_path)
    return new_file_name

def process_css_files(file_paths):
    renamed_files = []
    for file_path in file_paths:
        new_file_name = rename_css_file(file_path)
        renamed_files.append(new_file_name)
    return renamed_files

if __name__ == "__main__":
    css_file_paths = [
        "C:\xampp\htdocs\PilarEaseDJO\main\static\css\custom.css",
        "C:\xampp\htdocs\PilarEaseDJO\main\static\css\custom-footer.css"   # Update this path
    ]
    new_file_names = process_css_files(css_file_paths)
    print(f"New CSS file names: {new_file_names}")
