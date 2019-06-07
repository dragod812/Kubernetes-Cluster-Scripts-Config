echo "installing docker"
apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update && apt-get install -y docker-ce #fix a docker-ce version after testing

echo "installing kubeadm and kubectl"
apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl

#set kube-token an discovery hash based on the master node output
export KUBE_MASTER_IP=172.31.19.29
export KUBE_TOKEN=ggreif.4m6n41rvdiqz2t8n
export KUBE_DISCOVERY_HASH=sha256:7b7b0218c6cf855bca9fbd86d8e8255d35decb63951131176615e786b587ed99

#specify based on the master join output
kubeadm join $KUBE_MASTER_IP:6443 --token $KUBE_TOKEN --discovery-token-ca-cert-hash $KUBE_DISCOVERY_HASH
