FROM python:alpine

WORKDIR /app

COPY . .

EXPOSE 27004 27003

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python" , "R1DinningHole.py"]