FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r ./frontend/requirements.txt

EXPOSE 4444
CMD streamlit run index.py --server.port 4444