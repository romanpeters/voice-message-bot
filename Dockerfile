FROM python:3.7

ADD . /bot
WORKDIR /bot
RUN apt update && apt install -y ffmpeg
RUN pip install --no-cache-dir -U -r requirements.txt

CMD ["python", "-u", "main.py"]