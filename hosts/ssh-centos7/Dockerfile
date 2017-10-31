# "ported" by Adam Miller <maxamillion@fedoraproject.org> from
#   https://github.com/fedora-cloud/Fedora-Dockerfiles
#
# Originally written for Fedora-Dockerfiles by
#   scollier <scollier@redhat.com>

FROM centos:latest
MAINTAINER 2nd division commander  <2nd.div.commander@gmail.com>

RUN yum -y update; yum clean all
RUN yum -y install openssh-server sudo passwd; yum clean all
RUN echo "nyobi ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/nyobi && \
    chmod 0440 /etc/sudoers.d/nyobi

ADD ./start.sh /start.sh
RUN mkdir /var/run/sshd
# SSH login hack. Otherwise user is kicked off automaticaly after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N '' 

RUN chmod 755 /start.sh
#EXPOSE 22
RUN ./start.sh
ENTRYPOINT ["/usr/sbin/sshd", "-D"]
