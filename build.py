import os
import shutil
import zipfile

from PyInstaller.__main__ import run


def copy_assets():
    shutil.copytree(
        "assets/face_recognition_models",
        "dist/E-Aigaq/_internal/face_recognition_models",
    )
    os.makedirs("dist/E-Aigaq/_internal/assets", exist_ok=True)
    shutil.copytree("assets/fonts", "dist/E-Aigaq/_internal/assets/fonts")


def create_zip():
    zip_file_path = os.path.join("dist", "E-Aigaq.zip")
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("dist/E-Aigaq"):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, "dist"))


if __name__ == '__main__':
    options = [
        '--windowed',
        '--name=E-Aigaq',
        '--icon=assets/icon.png',
        'main.py',
    ]
    run(options)

    copy_assets()

    create_zip()

    print("Сборка завершена, файлы скопированы и создан zip-архив.")
