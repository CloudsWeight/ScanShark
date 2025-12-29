FROM node:23-bookworm

WORKDIR /app
COPY /app .
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
RUN apt-get update -y 
RUN apt-get upgrade -y
RUN apt install -y python3-pip sudo 
RUN rm /usr/lib/python3.11/EXTERNALLY-MANAGED
RUN sudo pip install -r requirements.txt
EXPOSE 3333
RUN sudo pip freeze
CMD ["python3", "src/main.py"]
