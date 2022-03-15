#!/bin/sh

echo "Commiting streak image"
PYTHON_ENV=$(python -c "import sys; sys.stdout.write('1') if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else sys.stdout.write('0')")

if [ $PYTHON_ENV -eq 0 ]
then
  echo "Not in virtual env. Not going to try to create streak image"
  exit
fi

diff= exec git diff --cached --name-only --diff-filter=ACM

git add $PWD/media/streak.jpg
git commit --amend --no-verify $PWD/media/streak.jpg
