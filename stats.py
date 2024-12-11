import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# Path to the Zsh history file
history_file = f"{str(Path.home())}/.zsh_history"
stats_dir = Path.home() / "stats"
stats_dir.mkdir(exist_ok=True)  # Ensure the stats directory exists

# Get the timestamp for 7 days ago
seven_days_ago = datetime.now() - timedelta(days=7)
seven_days_ago_unix = int(seven_days_ago.timestamp())

# Initialize counters and lists
commands_stats = {
    "git_checkout_b": [],
    "git_commit": 0,
    "git_push": 0,
    "docker_commands": 0,
    "make_commands": 0,
}
all_commands = []

# Regex to validate branch names
branch_name_pattern = re.compile(r"^[a-zA-Z0-9/_:-]+$")

# Parse the Zsh history file
with open(history_file, 'rb') as file:  # Open in binary mode
    for line in file:
        try:
            # Decode the line while ignoring errors
            line = line.decode('utf-8', errors='ignore').strip()
            if line.startswith(":") and ":0;" in line:
                # Extract timestamp and command
                parts = line.split(":0;")
                timestamp = int(parts[0].strip(":"))
                command = parts[1].strip()

                # Check if the timestamp is within the last 7 days
                if timestamp >= seven_days_ago_unix:
                    # Record the command
                    all_commands.append(command)

                    # Categorize commands
                    if "git checkout -b" in command:
                        branch_name = command.split("git checkout -b")[1].strip()
                        if branch_name_pattern.match(branch_name):  # Validate branch name
                            commands_stats["git_checkout_b"].append(branch_name)
                    elif "git commit" in command:
                        commands_stats["git_commit"] += 1
                    elif "git push" in command:
                        commands_stats["git_push"] += 1
                    elif "docker" in command:
                        commands_stats["docker_commands"] += 1
                    elif "make" in command:
                        commands_stats["make_commands"] += 1
        except (ValueError, IndexError):
            continue

# Count most frequently used commands
top_commands = Counter(all_commands).most_common(5)

# Get the current month for file naming
current_month = datetime.now().strftime("%b").lower()  # Example: jan, feb
stats_file = stats_dir / f"developer_stats_{current_month}.txt"

# Prepare the stats content
date_range = f"{seven_days_ago.strftime('%d %b %Y')} to {datetime.now().strftime('%d %b %Y')}"
content = "\n"
content += "=" * 50 + "\n"
content += f"Developer Activity from {date_range}\n"
content += "=" * 50 + "\n\n"

# Git branches created
content += "Git Branches Created:\n"
if commands_stats["git_checkout_b"]:
    for branch in commands_stats["git_checkout_b"]:
        content += f"  - {branch}\n"
else:
    content += "  No branches created.\n"

content += "\nSummary Table:\n"
content += "=" * 50 + "\n"
content += f"{'Metric':<30}{'Count':>20}\n"
content += "=" * 50 + "\n"
content += f"{'Git Branches Created':<30}{len(commands_stats['git_checkout_b']):>20}\n"
content += f"{'Git Commits':<30}{commands_stats['git_commit']:>20}\n"
content += f"{'Git Pushes':<30}{commands_stats['git_push']:>20}\n"
content += f"{'Docker Commands':<30}{commands_stats['docker_commands']:>20}\n"
content += f"{'Make Commands':<30}{commands_stats['make_commands']:>20}\n"
content += "=" * 50 + "\n\n"

content += "Top 5 Most Used Commands:\n"
content += "=" * 50 + "\n"
for cmd, count in top_commands:
    content += f"  {cmd:<40} {count:>8}\n"
content += "=" * 50 + "\n"

# Write or append to the stats file
if stats_file.exists():
    # Append to the file if it exists
    with open(stats_file, "a") as f:
        f.write(content)
else:
    # Create a new file and write
    with open(stats_file, "w") as f:
        f.write(content)
