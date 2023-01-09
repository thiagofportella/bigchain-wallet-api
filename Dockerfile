FROM python:3.9
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python app.py
