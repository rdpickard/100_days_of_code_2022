#!/bin/sh

if [ -e .day_8_no_verfify_doent_work_with_post_commit_hack_file_to_avoid_looping_forrever ]
    then
      rm .day_8_no_verfify_doent_work_with_post_commit_hack_file_to_avoid_looping_forrever
      echo "Committing streak image"
      git commit --no-verify --amend  $PWD/media/streak.jpg
fi
