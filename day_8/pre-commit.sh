#!/bin/sh

echo "Creating commit streak image"
PYTHON_ENV=$(python -c "import sys; sys.stdout.write('1') if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else sys.stdout.write('0')")

if [ $PYTHON_ENV -eq 0 ]
then
  echo "Not in virtual env. Not going to try to create streak image"
  exit
fi

touch .day_8_no_verfify_doent_work_with_post_commit_hack_file_to_avoid_looping_forrever

mkdir -p $PWD/media/

# Create the streak image
python $PWD/day_6/commit_streak_image_generator.py $PWD  $PWD/media/streak.jpg
git add $PWD/media/streak.jpg