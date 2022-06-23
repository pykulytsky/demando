import subprocess


def main():
    cmd = ["uvicorn", "--app-dir", "src/", "main:app", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]

    subprocess.run(cmd)
