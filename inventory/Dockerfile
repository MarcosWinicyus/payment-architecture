FROM tiangolo/uvicorn-gunicorn:python3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY /inventory/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app