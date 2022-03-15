#!/bin/sh

if [ -e .commit ]
    then
      rm .commit
      echo "Committing streak image"
      git commit --no-verify --amend  $PWD/media/streak.jpg
fi
