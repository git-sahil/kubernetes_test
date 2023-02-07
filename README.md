# kubernetes_test
Repository for testing k8s code

There is a simple python flask application written in build-docker/app.py
Docker image will be built on top of this and used by k8s pod (spec.template.container.image) field under deployment

Start the deployment sequence by executing "run.sh"

This will build docker image for python flask application and use kustomize(built-in within k8s from 1.14 onwards) to create deployment and supporting service

Note:-
Requires a postgres db server already running(to store persistent data beyond the life of the application, since deployment's pod data is ephimeral). If not, you need to update the complete db connection uri with username and password in kustomize/overlay/dev/secrets.yml -> database-secret.uri field before running "run.sh"

An alternative to this can be to deploy database on k8s itself which requires a storage class to be defind(which depeneds on the underlying architecture on which k8s is deployed and which CSI it supports) and use this Storage class to create PVCs(on top of PVs), preferably dynamic PVCs.
Since, the assumed scope of this assignment was limited to the application part. Hence, database part is skipped.

Another alternative(not recommended) can be to use a /tmp/test.db file based database and mount using a PVC. This is left upto to the user's choice.

Another important point is that, "run.sh" is asking for some sensitive information(silently). The best practices, however, suggests to store these credentials:
a) If a vault is available: In a vault kv store and retrieve dynamically using "vault login" and "vault read" or "vault get" commands 
b) If using CI/CD pipelines with no vault access: E.g. Gitlab/Jenkins, Then as protected and masked / Credentials parameters respectively and create k8s secrets using CI/CD automation by retrieve those params values.

Pre-requisites:
1. A linux environment with k8s installed and context already set for kubectl.
2. Using kubectl 1.14+
3. Docker already installed and able to access docker.io (since python:3.8 will be pulled as base to create a custom docker image)

P.S: I've just finished writing the code. Haven't tested it myself due to shortage of time :P
Feel free to get back for any related Qs / concerns :)

