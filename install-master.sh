cho "installing docker"
apt-get update
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update && apt-get install -y docker-ce #fix a docker-ce version after testing

echo "installing kubernetes"
apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl

echo "deploying kubernetes (with calico)..."
kubeadm init  # add --apiserver-advertise-address="ip" if you want to use a different IP address than the main server IP
export KUBECONFIG=/etc/kubernetes/admin.conf

kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

#this output is required for bootstrapping worker nodes
#kubeadm join 172.31.15.185:6443 --token ufb5x1.2cb6ykv3hlxeo9bf --discovery-token-ca-cert-hash sha256:bc276abf6163ce730eadb59fa10818dd92e48811571a0c288c3a0e90215ed9bc
