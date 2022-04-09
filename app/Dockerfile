FROM python:3.9-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers vim
COPY ./req.txt /app/req.txt
RUN pip install --upgrade pip
RUN pip install -r /app/req.txt
COPY . /app
