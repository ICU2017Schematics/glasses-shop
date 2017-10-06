FROM python:2.7.14-alpine3.6
    
RUN pip install Flask Flask-Cache Flask-Cors requests

# application source code including static files, templates, etc
ADD src /app/src

EXPOSE 5000

ENTRYPOINT ["python", "-u", "/app/src/app.py"]
