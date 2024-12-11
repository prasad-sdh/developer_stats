# Developer stats

This project automates the generation of weekly developer activity statistics from your shell history. It summarizes commands such as:
- `git checkout -b` (branches created)
- `git commit` (total commits)
- `git push` (total pushes)
- Docker commands
- Make commands

## How It Works
- Extracts relevant commands from `~/.zsh_history` for the past 7 days.
- Appends to a monthly stats file in `~/stats/` or creates a new one for a new month.

## Setup
1. Place the script in your desired directory.
2. Ensure the `~/stats` directory exists (it will be created automatically if missing).
3. Add a cron job to run every Friday at 05:00 PM:
   ```bash
   crontab -e
   ```
   Add the following line:
   ```bash
   00 17 * * 5 /path/to/python /path/to/stats.py
   ```

## Example Output
File: `~/stats/developer_stats_jan.txt`
```
==================================================
Developer Activity from 01 Jan 2023 to 07 Jan 2023
==================================================

Git Branches Created:
  - feature/add-logging
  - bugfix/resolve-crash

Summary Table:
==================================================
Metric                                Count
==================================================
Git Branches Created                      2
Git Commits                               5
Git Pushes                                3
Docker Commands                           2
Make Commands                             1
==================================================
```

