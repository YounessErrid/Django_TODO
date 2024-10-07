FROM python:3.12.3-alpine

# RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "entrypoint.sh"]
