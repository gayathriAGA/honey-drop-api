FROM python:3.13-alpine
WORKDIR /var/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
COPY . .
RUN rm -rf db.sqlite3 && mkdir db
CMD ["sh", "-c", "python manage.py migrate && gunicorn honeydrop.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120"]