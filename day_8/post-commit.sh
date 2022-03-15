#!/bin/sh

echo "Commiting streak image"
PYTHON_ENV=$(python -c "import sys; sys.stdout.write('1') if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else sys.stdout.write('0')")

if [ $PYTHON_ENV -eq 0 ]
then
  echo "Not in virtual env. Not going to try to create streak image"
  exit
fi

git commit --no-verify --amend  $PWD/media/streak.jpg
