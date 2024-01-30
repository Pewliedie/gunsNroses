from PyInstaller.__main__ import run

if __name__ == '__main__':
    # Add your PyInstaller options here
    options = [
        '--onefile',  # Create a single executable file
        '--windowed',  # Run the program without a console window
        '--name=proof_vault',  # Set the name of the executable file
        '--icon=icon.ico',  # Set the icon file for the executable
        'main.py',  # Specify the main Python script to be bundled
    ]

    # Run PyInstaller
    run(options)
