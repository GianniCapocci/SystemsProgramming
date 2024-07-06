FROM python:3.8

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

EXPOSE 5000

CMD ["./start.sh"]
