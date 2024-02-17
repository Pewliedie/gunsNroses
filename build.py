from PyInstaller.__main__ import run

if __name__ == '__main__':
    options = [
        '--windowed',
        '--name=E-Aigaq',
        '--icon=assets/icon.png',
        'main.py',
    ]

    run(options)
