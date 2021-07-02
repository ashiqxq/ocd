FROM ubuntu

RUN apt update

RUN apt install python3.8 -y
RUN apt-get install python3-pip -y

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]