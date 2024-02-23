import subprocess

subprocess.run(["isort", "."])
subprocess.run(["black", "-S", "."])
