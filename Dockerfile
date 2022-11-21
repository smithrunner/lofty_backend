FROM python:3.9

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8080

# runs the production server
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "127.0.0.1:8080"]