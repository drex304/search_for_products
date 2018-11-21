# Pull base image
FROM python:3.7

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
#RUN pyenv install $(cat .python-version)
RUN pip install --upgrade pip
RUN pip install pipenv
COPY . /code/
RUN pipenv install --deploy

VOLUME /tmp

RUN pipenv run python /code/searcher/manage.py migrate
CMD ["pipenv", "run", "python", "/code/searcher/manage.py", "runscript", "process_products"]

