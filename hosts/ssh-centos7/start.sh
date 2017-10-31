#!/bin/bash

__create_user() {
# Create a user to SSH into as.
useradd nyobi
SSH_USERPASS=thelogock
echo -e "$SSH_USERPASS\n$SSH_USERPASS" | (passwd --stdin nyobi)
echo ssh user password: $SSH_USERPASS
}

# Call all functions
__create_user
