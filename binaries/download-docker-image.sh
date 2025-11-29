#!/bin/sh
# This script pulls docker image of the OVL (ogamma/logger) from Docker Hub and saves it in .tar.gz file.
imageName=ogamma/logger:latest
fileName=ovl-latest.tar.gz
echo "Pulling image $imageName from Doker Hub ..."
docker pull docker.io/$imageName
if [ $? == 0 ]; then
  echo "Saving image $imageName in archive file $fileName..."
  docker save $imageName | gzip -9 > $fileName
  if [ $? == 0 ]; then
    echo "Done"
    echo "To load the image from file $fileName on another machine offline, run the command:"
    echo "gunzip -c $fileName | docker load"
  else
    echo "Failed to save the image $imageName in file $fileName"
    exit 2
  fi
else
  echo " Failed to pull the image $imageName"
 exit 1
fi