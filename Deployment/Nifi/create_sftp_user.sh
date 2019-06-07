#first enable ssh for your machine
#as sudo user
#add new user, it will ask for password and set password
useradd nifi-test
#copy the data into the /home/nifi-test/ directory
#give ownership of data to the given group
chown -R nifi-test:nifi-test /home/nifi-test/data

#add the following lines to end of /etc/ssh/sshd_config
#Match user nifi-test
#	PasswordAuthentication yes

#restart ssh service
sudo service ssh restart
