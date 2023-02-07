FROM python:3.8
WORKDIR /app
COPY app.py /app
RUN pip install flask flask_sqlalchemy waitress
CMD ["python", "app.py"]
