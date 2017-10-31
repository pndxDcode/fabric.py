ssh -p $PORT root@localhost
- password is `screencast`


### fabric
 sumble accross a problem when tried to replace the database server
 the paramiko (ssh) is automaticaly assign ssh-key to known-host in ~/.ssh/known-hosts
 so when tried to replaced the old database server with the new one but with the same address 172.17.0.3
 it trew an exeption error like mith or something.
 work around for this problem is to remove the old ssh-known-hosts in ~/.ssh/known-hosts, and generate a new one

### 'ssh-keygen -R 172.17.0.3' // replaced the old known-hosts with the new one
- docker run -d -p 22 centos7-ssh:1
### ssh -p $PORT nyobi@localhost
### install sudo and add sudoers to user nyobi
### latest build centos7-ssh:5
- docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name 
- 'docker run -d -p 22 --rm --name centos7-ssh{1-3} centos7-ssh:5'
