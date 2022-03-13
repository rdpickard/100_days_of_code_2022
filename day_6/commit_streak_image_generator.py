
import sys

import git
import arrow
import imgkit

if len(sys.argv) != 3:
    print("Usage: python commit_streak_image_generator.py /path/to/git/repo /path/to/image/file")
    sys.exit(-1)

repo_dir = sys.argv[1]

repo = git.Repo(repo_dir)

commit_days = []

for commit in list(repo.iter_commits('main')):
    day = arrow.get(commit.committed_date).replace(hour=0, minute=0, second=0)
    if day not in commit_days:
        commit_days.append(day)

last_day = commit_days[0]
max_streak = 1
for commit_day in commit_days[1:]:
    if commit_day == last_day.shift(days=-1):
        max_streak += 1
    else:
        max_streak = 1
    last_day = commit_day

imgkit.from_string(f'<h1>{max_streak} day streak!</h1>', sys.argv[2])

