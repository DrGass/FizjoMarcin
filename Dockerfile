# 
FROM python:3.11.3

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt


# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./alembic.ini /code/alembic.ini

# 
COPY ./app /code/app

#
ENV PYTHONPATH "${PYTHONPATH}:/code/app"

#


# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
