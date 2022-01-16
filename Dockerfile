FROM python:3.8-slim

WORKDIR /home/

COPY . /home/

RUN ls -la /home
RUN pip install --quiet --upgrade pip
RUN pip install  pipenv
RUN pipenv install -r /home/requirements.txt

ENV PYTHONPATH /home

CMD [ "pipenv", "run", "python", "-m", "flask", "run"]