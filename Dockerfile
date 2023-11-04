FROM python:3.10-slim-buster
ENV PYTHONPATH /app
ADD . /app
WORKDIR /github/workspace
# RUN pip install PyGithub
# 安装 git
RUN apt-get update && apt-get install -y git

CMD [ "python3", "/app/main.py" ]

