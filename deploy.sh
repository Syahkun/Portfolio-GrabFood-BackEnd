#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
sudo docker stop flask-tutorial
sudo docker rm flask-tutorial
sudo docker rmi syahkun/flask-tutorial:latest
sudo docker run -d --name flask-tutorial -p 5000:5000 syahkun/flask-tutorial:latest
