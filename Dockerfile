FROM python:3.7-slim
ADD . /code
RUN chmod +x /code/entrypoint.sh
WORKDIR /code
RUN pip install -r requirements.txt
RUN python -m pytest
CMD ["sh", "entrypoint.sh"]