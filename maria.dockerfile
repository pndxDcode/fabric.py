FROM centos:latest

MAINTAINER "2nd division commander <2nd.div.commander>

# Install MariaDB
ADD config/MariaDB.repo /etc/yum.repos.d/MariaDB.repo
RUN yum update -y
RUN yum install sudo -y MariaDB-server MariaDB-client

RUN echo "nyobi ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/nyobi && \
    chmod 0440 /etc/sudoers.d/nyobi

ADD ./start.sh /start.sh
# Configure MariaDB
ADD config/my.cnf /etc/my.cnf

# All the MariaDB data that you'd want to backup will be redirected here
RUN mkdir /data
VOLUME ["/data/mariadb"]

# SSH login hack. Otherwise user is kicked off automaticaly after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''


# Port 3306 is where MariaDB listens on
EXPOSE 3306

# These scripts will be used to launch MariaDB and configure it
# securely if no data exists in /data/mariadb
ADD config/mariadb-start.sh /opt/bin/mariadb-start.sh 
ADD config/mariadb-setup.sql /opt/bin/mariadb-setup.sql
RUN chmod u=rwx /opt/bin/mariadb-start.sh
RUN chown mysql:mysql /opt/bin/mariadb-start.sh /opt/bin/mariadb-setup.sql /data/mariadb

# run all subsequent commands as the mysql user
USER mysql

ENTRYPOINT ["/opt/bin/mariadb-start.sh"]
