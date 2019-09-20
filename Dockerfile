FROM python:3.6

COPY ./requirements.txt /app/requirements.txt
COPY ./package.json /app/package.json

WORKDIR /app

RUN pip install -r requirements.txt && \
    curl -sL https://deb.nodesource.com/setup_11.x | bash - && \
    apt-get install -y nodejs && \
    npm install

COPY . /app
