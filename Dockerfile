FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt update && apt-get install libssl-dev libicu-dev software-properties-common wget ffmpeg python3-pip -y 

#RUN apt update && apt-get upgrade -y
#RUN apt install libssl-dev libicu-dev software-properties-common wget -y
#RUN apt install libicu-dev -y
#RUN apt install software-properties-common -y
#RUN apt install wget -y
#RUN apt install zip unzip -y
#RUN apt update && apt-get upgrade -y
#RUN apt install ffmpeg -y
#RUN apt install python3-pip -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","fileconvNO.py"]

