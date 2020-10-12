FROM python:3.7-alpine

COPY app/initApi.py /app/
COPY app/favretweet.py /app/
COPY req.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "retweetFromThirds.py"]
