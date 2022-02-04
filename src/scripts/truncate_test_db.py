import subprocess


def main():
    cmd = ["python", "src/commands.py", "truncate-test-db"]
    subprocess.run(cmd)
