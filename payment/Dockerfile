FROM tiangolo/uvicorn-gunicorn:python3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY /payment/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app