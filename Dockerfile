# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Set the working directory
WORKDIR /web

# Copy the requirements file
COPY requirements.txt .

# Install dependencies including uwsgi
RUN apt-get update \
    && apt-get install -y netcat \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpcre3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential python3-dev libpcre3-dev \
    && rm -rf /var/lib/apt/lists/*


# copy the project code
COPY . .

# prepare scripts to run
#COPY ./basesite/fixtures/install_fixtures.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
#RUN sed -i 's/\r$//g' install_fixtures.sh
RUN chmod +x entrypoint.sh
#RUN chmod +x install_fixtures.sh

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose the application port
EXPOSE 8080

# Entrypoint: wait for postgres
ENTRYPOINT ["/web/entrypoint.sh"]