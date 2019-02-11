FROM python:3.6-slim

ENV PORT=8080
WORKDIR /dojo-task
COPY ./requirements.txt /dojo-task
RUN pip3 install -r /dojo-task/requirements.txt
COPY ./ /dojo-task
EXPOSE $PORT

CMD ["python3", "server.py"]
