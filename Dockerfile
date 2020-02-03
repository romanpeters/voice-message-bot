FROM python:3.7

COPY . /bot
WORKDIR /bot
RUN pip install --no-cache-dir -U -r requirements.txt

CMD ["python", "-u", "main.py"]