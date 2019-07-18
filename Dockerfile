FROM centos/python-36-centos7

USER root
RUN yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
RUN yum install -y docker-ce

RUN pip install docker
ADD dummy_registry.py .

ENTRYPOINT ["./dummy_registry.py"]
