# 
FROM python:3.11.3

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
# COPY ./alembic.ini /code/alembic.ini

# 
# COPY ./app/ /code/

#
# ENV PYTHONPATH "${PYTHONPATH}:/code"


# 
CMD ["bash", "-c", "wait-for-it --service postgres:5432 --timeout 300 && ls &&cd app && python run.py"]
