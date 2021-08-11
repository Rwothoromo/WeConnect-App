# set base image (host OS)
FROM python:3.9.6-slim as base

# add everything in the current folder into a directory in the image called weconnect
ADD . /weconnect

# set the working directory in the container
WORKDIR /weconnect

# install dependencies
RUN pip install -r requirements.txt
