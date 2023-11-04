FROM python:3.10-slim-buster
ENV PYTHONPATH /app
ADD . /app
WORKDIR /github/workspace
# RUN pip install PyGithub

CMD [ "python3", "/app/main.py" ]

