# kubernetes_test
Repository for testing k8s code

There is a simple python flask application written in build-docker/app.py
Docker image will be built on top of this and used by k8s pod (spec.template.container.image) field under deployment

Start the deployment sequence by executing "run.sh"

This will build docker image for python flask application and use kustomize(built-in within k8s from 1.14 onwards) to create deployment and supporting service

Note:-
1. Upon executing "run.sh", it will ask for some sensitive information(silently). The best practices, however, suggests to store the credentials:
    a) If a vault is available: In a vault kv store and retrieve dynamically using "vault login" and "vault read" or "vault get" commands 
    b) If using CI/CD pipelines with no vault access: E.g. Gitlab/Jenkins, then store as protected and masked CI/CD variables under settings / Credentials parameters respectively and create k8s secrets using CI/CD automation by retrieve those params values dynamically.
2. Some lines are just commented. I was having several rough ideas, and when modifying, did not remove those lines completely. Could put them in another branch though. Nevertheless, we are only testing the approach I guess :P
3. A dummy tls certificate will be created by run.sh using openssl command (might ask for more information like DN,OU etc.). Again, we can fetch this dynamically in a CI/CD environment if having access to a vault. Usually, this must belong to the domain where app is running and can be added to the ingress resource for the app if ingress controller already installed (Not in current scope)

Pre-requisites:
1. A linux environment with k8s installed and context already set for kubectl.
2. Using kubectl 1.14+
3. Docker already installed and able to access docker.io (since python:3.8 will be pulled as base to create a custom docker image)
4. Requires a postgres db server already running(to store persistent data beyond the life of the application, since deployment's pod data is ephimeral).
    If not, you need to update the complete db connection uri with username and password in kustomize/overlay/dev/secrets.yml -> database-secret.uri field before running "run.sh"

    An alternative to this can be to deploy database on k8s itself which requires a storage class to be defind(which depeneds on the underlying architecture on which k8s is deployed and which CSI it supports) and use this Storage class to create PVCs(on top of PVs), preferably dynamic PVCs.
    Since, the assumed scope of this assignment was limited to the application part. Hence, database part is skipped.

    Another alternative(not recommended) can be to use a /tmp/test.db file based database and mount using a PVC. This is left upto to the user's choice.
5. openssl already installed and available under $PATH


P.S: I've just finished writing the code. Haven't tested it myself due to lack of environment and shortage of time :P
We can test this together if we get the chance.
Feel free to get back for any related Qs / concerns :)

