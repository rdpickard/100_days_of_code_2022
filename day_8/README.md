# Git Pre-commit script to create streak image
---
```
Language: Bash
Brief: Script to create media/streak.jpg automatically on commit
Scope: 
Tags: low effort
State: 
Result: 
```
---

Create a script to run the project from day_6 automatically on commit. 

Because this bash script will use the virtualenv of the 100 days project, this idea would generally be frowned upon by the folks who sheppard Git

![](media/screen_shot_1.png)
lol.
[Activate virtualenv in hook template #1522](https://github.com/pre-commit/pre-commit/issues/1522)

But since this 100 days endeavor is just a playground for ideas, I am going to ignore that good advice.

### Results

LOLs all around. I get why doing _clever boy_ tricks in git hooks isn't a great idea.

It does work, but there is an ugly hack to avoid an infinite loop that is caused by post-commit script being called even if --no-verrify is passed to `git commit`.

Still, it does work.

### Notes
(NOOP to trigger commit)

(NOOP to trigger commit)
(NOOP)

(NOOP)

### If I was to do more
I would do something else