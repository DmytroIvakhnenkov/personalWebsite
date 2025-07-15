import subprocess

repo_path = "/home/dmytro/BigDmytro/personalWebsite"

# Run the csvProcessing script
subprocess.run(["python3", "csvProcessing.py"], cwd=repo_path)

# Git operations
subprocess.run(["git", "add", "."], cwd=repo_path)
subprocess.run(["git", "commit", "-m", "Hourly update"], cwd=repo_path)
subprocess.run(["git", "push"], cwd=repo_path)