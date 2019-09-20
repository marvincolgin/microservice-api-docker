FROM alpine:3.1

# Update
RUN apk add --update python py-pip

COPY ./ ./src/

WORKDIR ./src

# Install app dependencies
RUN ls -l .
RUN ls -l ./src/
RUN pip install -r requirements.txt

EXPOSE  8000
CMD ["python", "./src/index.py", "-p 8000"]
