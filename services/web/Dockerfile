# pull official base image for python
FROM python:3.9.0-slim-buster

# set the work directory
WORKDIR /opt/app

# set the environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip && pip install wheel
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/opt/app/entrypoint.sh"]
