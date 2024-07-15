# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Locust and any other dependencies,
RUN pip install locust
RUN pip install beautifulsoup4
RUN pip install locust psycopg2-binary
RUN pip install odoorpc


# Command to run Locust
CMD ["locust", "-f", "/mnt/locust/502.py", "--host=http://ecs-lb-1919862548.ap-south-1.elb.amazonaws.com/"]
#CMD ["locust", "-f", "/mnt/locust/locust.py"]