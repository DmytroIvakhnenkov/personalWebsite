import subprocess
from datetime import datetime

repo_path = "/home/dmytro/BigDmytro/personalWebsite"

# Run the csvProcessing script
subprocess.run(["python3", "csvProcessing.py"], cwd=repo_path)

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:00")
# Git operations
subprocess.run(["git", "add", "."], cwd=repo_path)
subprocess.run(["git", "commit", "-m", f"chore: update worked hours for {timestamp}"], cwd=repo_path)
subprocess.run(["git", "push"], cwd=repo_path)