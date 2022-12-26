FROM python:latest

COPY . .

RUN pip install selenium

RUN pip install requests

CMD ["python","scraper_class.py"]