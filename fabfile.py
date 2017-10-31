"""this example use python fabric to deploy mysql/mariadb and apache on five containers"""


# import all the fabric functions that we need explicitly
from fabric.api import env, roles, sudo, execute, put, run, local, lcd, prompt, cd, parallel

# import the os module to get file basenames
import os

# define groups of webservers and databases
env.roledefs ={
        "webserver" : ["nyobi@172.17.0.2", "nyobi@172.17.0.4","nyobi@172.17.0.5"],
        "database"  : ["nyobi@172.17.0.3", "nyobi@172.17.0.6"],
        }
# define a special group called all so we can easily send out commands to all servers if needed
env.roledefs["all"] = [h for r in env.roledefs.values() for h in r]

#the packages that are required to run our application on the server groups
packages_required = {
        "webserver" : [  "httpd","php", "ntp", "php-mysqli"],
        "database"  : ["mariadb-server"]
        }

# files that need to be downloaded from the labserver repo
download_files = {
        "databases" : ["http://labfiles.linuxacademy.com/python/fabric/sakila.sql",
                        "http://labfiles.linuxacademy.com/python/fabric/sakila-data.sql"],
        "webserver" : ["http://labfiles.linuxacademy.com/python/fabric/index.php"]
        }

@roles("database") # this decorater will make the fuction following it run for all database group server
def install_database():
    # install the database application
    # sudo for superuser on remote server
    sudo ("yum -y install %s" % " ".join(packages_required["database"]),pty=True)

    #activate MySQL/MariaDB in the system control
    sudo("systemctl enable mariadb",pty=True)

    # start MySQL/MariaDB using the system control
    sudo("systemctl start mariadb",pty=True)

    # Create a user on the database that we will be using from our webservers
    sudo(r""" mysql -h localhost -u root -e "CREATE USER 'web'@'%' IDENTIFIED BY 'web'; GRANT ALL PRIVILEGES ON *.* TO 'web'@'%'; FLUSH PRIVILEGES; " """)

    # Check fo the mysql running process 
    run("ps -ef | grep myqsl")
@parallel
@roles("database") # this decorator will make the function following it run for all database group server
def setup_database():
    #setup the tmp directory where we will download files from the web 
    tmpdir = "/tmp"

    # this cd is the fabric command to change directory on the remote server 
    with cd(tmpdir): #cd changes the dir on the remote server 
        
        #iterate over the files we need to download for the datbaase
        for url in download_files["database"]:
            # basename gives us just the name of the file, without any path info, it also works for urls
            filename = "%s/%s" %(tmpdir, os.path.basename(url));

            #using the function run on the remote server, we can execute commands, in this case wget which open the rl and save it
        #o filename
            run("wget --no-cache %s -O %s" % (url, filename))

            #since these are SQL files, we can just dump them into out MySQL/MariaDB server
            run("mysql -u root < %s" % filename)
@roles("webserver") # this decorator will make the function following it run for all webserver group server
def install_webserver():
    #install the webserver applications
    sudo("yum -y install %s" % " ".join(packages_required["webserver"]),pty=True)

    #active and start httpd
    sudo("systemctl enable httpd.service", pty=True)
    sudo("systemctl start httpd.service", pty=True)

    # here are some SELinux commands to get this working
    sudo("setsebool -P httpd_can_network_connect=1", pty=True)
    sudo("setsebool -P httpd_read_user_contect=1", pty=True)
@roles("webserver") # this decorator will make the fuction following it run for all webserver group server 
def setup_webserver():
    #setup the tmp directory where we will download files from the web 
    tmpdir = "/tmp"

    # directory on the remote server 
    remote = "/var/www/html"

    # this time we will download the files on our master sever and then put them on the ermote server to see the functionality
    with lcd(tmpdir):
        # iterate over the files we need to download for the webserver
        for url in download_files["webserver"]:
            # basename gives us just the name of the file, without any path info, it also works for urls 
            filename = "%s/%s" %(tmpdir, os.path.basename(url));

            # local runs the command locally on our local server
            local("wget --no-cache %s -O %s" %(url, filename)) 

            # and put sends a file from the local server to the remote server
            # we can also change the running permission
            # and use sudo if required 
            put(filenme, "/var/www/html", mode=0755, use_sudo=True)

    # the webserver need to conect to a database in the back
    database = pick_server(env.roledefs["database"])

    # again using sudo, we can just create a file on the remote servver,
    # and put in the database server we got back from the fuction
    sudo(r""" echo " <?php \\$db = '%s'; ?> "> /var/www/html/db.php """ % env.roledefs['database'][database])

def pick_server(mylist):
    # simple function that takes a list and enumerates it
    # and asks the user to select a valid member from the list
    database = 0
    while not 1<=database<=len(mylist):
        for i, db in enumerates(mylist):
            print "[%s] - %s" %(i, db)
            database = prompt("Enter the number of the database should I connect %s to:  " % (env.host) , validate=int)
            return int(database)-1

@roles("all")
def upgrade_server():
    # Just doing a upgrade on the CentOS
    sudo("yum -y upgrade", pty=True)

# this is the main function we will be calling to get it all running
def deploy():
    # note here that the execute fuction has the names of the functions we 
    # are calling, but we ae excluding the parenthesis()
    execute(upgrade_server)
    execute(install_database)
    execute(install_webserver)
    execute(setup_database)
    execute(setup_webserver)
    print "we are done"
