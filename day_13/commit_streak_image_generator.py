import random
import sys
import base64
import os

import git
import arrow
import imgkit

if len(sys.argv) != 4:
    print("Usage: python commit_streak_image_generator.py /path/to/git/repo /path/to/pips /path/to/image/file")
    sys.exit(-1)

repo_dir = sys.argv[1]
pip_dir = sys.argv[2]
streak_file = sys.argv[3]

repo = git.Repo(repo_dir)

commit_days = []

for commit in list(repo.iter_commits('main')):
    day = arrow.get(commit.committed_date).to('local').replace(hour=0, minute=0, second=0)

    if day not in commit_days:
        commit_days.append(day)

last_day = commit_days[0]

# The commit order is from most recent to oldest. Reverse the list to get the most recent streak
commit_days.reverse()

max_streak = 1
for commit_day in commit_days[1:]:
    if commit_day == last_day.shift(days=1):
        max_streak += 1
    else:
        max_streak = 1
    last_day = commit_day

pip_files = [os.path.join(pip_dir, f) for f in os.listdir(pip_dir) if f.startswith("pip_") and f.endswith(".png") and os.path.isfile(os.path.join(pip_dir, f))]

pips_html_image_tags_as_string = []
for _ in range(0, max_streak):
    pip_file = pip_files[random.randrange(0, len(pip_files))]

    with open(pip_file, "rb") as pip:
        pip_base64 = base64.b64encode(pip.read())

    pips_html_image_tags_as_string.append(f'<img src="data:image/png;base64, {pip_base64.decode("utf-8")}" style="width:32px;height:32px;"/>\n')


image_html = f'<h1>{max_streak} day streak!</h1>\n'
for pip_tag in pips_html_image_tags_as_string:
    image_html += pip_tag

imgkit.from_string(image_html, streak_file)
