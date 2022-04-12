import subprocess


def main():
    cmd = ["uvicorn", "--app-dir", "src/", "main:app", "--workers", "4", "--reload"]
    subprocess.run(cmd)
