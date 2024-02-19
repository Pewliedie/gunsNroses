import os
import shutil

from PyInstaller.__main__ import run


def copy_assets():
    shutil.copytree(
        "assets/face_recognition_models", "dist/internal/face_recognition_models"
    )

    os.makedirs("dist/internal/assets", exist_ok=True)
    shutil.copytree("assets/fonts", "dist/internal/assets/fonts")


if __name__ == '__main__':
    options = [
        '--windowed',
        '--name=E-Aigaq',
        '--icon=assets/icon.png',
        'main.py',
    ]
    run(options)

    copy_assets()

    print("Сборка завершена и файлы скопированы.")
