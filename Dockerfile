# 
FROM python:3.11.3

# 
WORKDIR /FizjoMarcin

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /FizjoMarcin/app

#
ENV PYTHONPATH "${PYTHONPATH}:/"

# 
CMD ["uvicorn", "app.main:app"]
