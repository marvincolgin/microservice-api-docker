FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install -r requirements.txt

# Bundle app source
COPY ./api/index.py /api/index.py

EXPOSE  8000
CMD ["python", "/api/index.py", "-p 8000"]
