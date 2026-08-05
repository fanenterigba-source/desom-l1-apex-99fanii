FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD python desom_l1_ws.py & python -m http.server $PORT --bind 0.0.0.0
