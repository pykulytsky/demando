import subprocess


def main():
    cmd = ["python", "src/commands.py", "truncate_db"]
    subprocess.run(cmd)
