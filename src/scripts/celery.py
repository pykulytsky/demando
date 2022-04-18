import subprocess


def main():
    cmd = ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]
    subprocess.run(cmd)
