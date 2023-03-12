FROM python:3.10.4

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000 5000

ENTRYPOINT ["python", "_app_.py"]

VOLUME ./storage:/storage