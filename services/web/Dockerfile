###########
# BUILDER #
###########


# pull official base image for python
FROM python:3.9.0-slim-buster as builder

# set the work directory
WORKDIR /usr/src/app

# set the environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . .
RUN flake8 --ignore=E501,F401 .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image for python
FROM python:3.9.0-slim-buster

# flasker is the user that will own the application and run it in the container
# create the flasker user
RUN addgroup --system flasker && adduser --system --group flasker

# create a home directory for flasker user and 
RUN mkdir -p /home/flasker/web

# create the appropriate directories
ENV HOME=/home/flasker
ENV APP_HOME=/home/flasker/web
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder  /usr/src/app/wheels /wheels
COPY --from=builder  /usr/src/app/requirements.txt .
RUN pip install -U pip
RUN pip install --no-cache /wheels/*

# copy entrypoint
COPY ./entrypoint.sh $APP_HOME

# copy flaskr
COPY . $APP_HOME

# chown all the file to the flasker user
RUN chown -R flasker:flasker $APP_HOME

# run entrypoint.sh
ENTRYPOINT ["/home/flasker/web/entrypoint.sh"]
