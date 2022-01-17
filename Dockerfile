FROM python:3.8-slim

WORKDIR /home/

COPY . /home/

RUN ls -la /home
RUN pip install --quiet --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ENV PYTHONPATH /home
ENV FLASK_APP /home/app.py

EXPOSE 5000

#CMD ["python", "-m", "flask", "run"]

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]