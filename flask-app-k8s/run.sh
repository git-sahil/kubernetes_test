#!/bin/bash

# Define all global variables here
BUILD_DIR="build-docker"


# Build App
if [-d ${BUILD_DIR} ]
    then cd ${BUILD_DIR}
    # Using Kaniko
    kaniko build -t my-web-app:latest .
    kaniko copy app.py /app/

    cd ..
else
    echo "${BUILD_DIR} directory does not exist. Please check the name"; exit 1
fi

# Silently take user and password inputs from the terminal. If using any CI/CD tools, can be passed via environment variable parameters or better to retrieve from vault kv store
# But we are using simple yet efficient minikube ;) 
set -a mydbusr mydbpasswd dburl dbport dbname
printf "Enter postgres db username(Will not be echoed on terminal): "
read -s "mydbuser"
printf "Enter postgres db password(Will not be echoed on terminal): "
read -s "mydbpasswd"
printf "Enter postgres db url: "
read "dburl"
printf "Enter postgres db port: "
read "dbport"
printf "Enter db name"
read "dbname"

# Generate web security certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt
echo "`base64 tls.crt`" | tr -d '\n' > tls.crt.base64
echo "`base64 tls.key`" | tr -d '\n' > tls.key.base64

# Now update these values in secrets.yml
sed -e "s/DBUSERENV/${mydbuser}/" -e "s/DBPASSWORDENV/${mydbpasswd}/" -i ./base/secrets.yml

kubectl apply -k kustomize/overlay/dev
