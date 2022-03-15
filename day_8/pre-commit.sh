#!/bin/sh

echo "Creating commit streak image"
PYTHON_ENV=$(python -c "import sys; sys.stdout.write('1') if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else sys.stdout.write('0')")

if [ $PYTHON_ENV -eq 0 ]
then
  echo "Not in virtual env. Not going to try to create streak image"
  exit
fi

# Create the streak image
python $PWD/day_6/commit_streak_image_generator.py $PWD  $PWD/media/streak.jpg

# Commit the streak image
#git commit --amend --no-verify --message "new streak image" $PWD/media/streak.jpg