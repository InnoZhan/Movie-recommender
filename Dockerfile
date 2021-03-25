FROM python:3.8-alpine
COPY . /app
WORKDIR /app
EXPOSE 80
RUN pip install -r requirements.txt
CMD python server.py
