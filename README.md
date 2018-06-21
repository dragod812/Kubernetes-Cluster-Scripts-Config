# Kubernetes-Cluster-Scripts-Config
Kubernetes Cluster setup scripts and config files for deploying any application in containerized environment.
Following are the steps to create a local Single Master Cluster using Kubeadm:<br>
(**Kubeadm** is a tool built to provide kubeadm init and kubeadm join as best-practice “fast paths” for creating Kubernetes clusters.<br>
kubeadm performs the actions necessary to get a minimum viable cluster up and running.)<br>
1) Install Vagrant.(Go through the Prerequisites for vagrant)<br>
2) Create a directory and run the following commands in it:<br>
```vagrant init ubuntu/xenial64```<br>Go through the Vagrantfile and setup the configuration you need(refer Vagrantfile).<br>
```vagrant up```<br>
3) On the vagrant box run the install-kubernetes.sh script. Also run the create-user.sh script(if you don't have root access to the machine).<br>
4) By default, your cluster will not schedule pods on the master for security reasons.<br>
If you want to be able to schedule pods on the master, e.g. for a single-machine Kubernetes cluster for development, run:<br>
```
kubectl taint nodes --all node-role.kubernetes.io/master-
```
5) You can join other vagrant boxes connected in the same internal network(refer Vagrantfile) using a command like this:<br>
```
kubeadm join --token <token> <master-ip>:<master-port> --discovery-token-ca-cert-hash sha256:<hash>
```
