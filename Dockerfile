FROM python:3.9.6-alpine3.14

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD [ "python", "-u", "main.py" ]



