# Kubernetes-Cluster-Scripts-Config
## Kubernetes Setup On-Premise
```
# on master
sudo sh ./install-master.sh

#on slave
sudo sh ./install-node.sh

#Then run the join command
kubeadm join $KUBE_MASTER_IP:6443 --token $KUBE_TOKEN --discovery-token-ca-cert-hash $KUBE_DISCOVERY_HASH
```

## Kubernetes Setup using Vagrant
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
Following are the commands that will be useful in your kubernetes endevours:
1) ```kubectl get nodes```<br>
2) ```kubectl run kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1 --port=8080 ```<br>
3) ```kubectl get deployments ```<br>
4) ```kubectl proxy ```<br>
5) ```export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}') echo Name of the Pod: $POD_NAME ```<br>
6) ```kubectl get pods ```<br>
7) ```kubectl get services ```<br>
8) ```kubectl describe pods ```<br>
9) ```kubectl exec -ti $POD_NAME bash ```<br>
10) ```kubectl exec $POD_NAME env ```<br>
11) ```kubectl logs $POD_NAME  ```<br>
12) ```kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080 ```<br>
13) ```kubectl delete service -l run=kubernetes-bootcamp ```<br>
14) ```kubectl scale deployments/kubernetes-bootcamp --replicas=4 ```<br>
15) ```kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2 ```<br>
16) ```export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}') echo NODE_PORT=$NODE_PORT ```<br>
17) ```kubectl rollout status deployments/kubernetes-bootcamp ```<br>
