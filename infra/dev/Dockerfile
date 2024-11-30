FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app/bot_api

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
