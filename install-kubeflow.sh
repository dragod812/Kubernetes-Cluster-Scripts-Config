echo "installing ksonnet"
export KS_VER=0.13.1
export KS_PKG=ks_${KS_VER}_linux_amd64
wget -O /tmp/${KS_PKG}.tar.gz https://github.com/ksonnet/ksonnet/releases/download/v${KS_VER}/${KS_PKG}.tar.gz
mkdir -p ${HOME}/bin
tar -xvf /tmp/$KS_PKG.tar.gz -C ${HOME}/bin
export PATH=$PATH:${HOME}/bin/$KS_PKG

echo "installing kubeflow"
export KUBEFLOW_SRC=/home/ubuntu/kubeflow
export KFAPP=kf_app
mkdir ${KUBEFLOW_SRC}
cd ${KUBEFLOW_SRC}
export KUBEFLOW_TAG=v0.4.1
curl https://raw.githubusercontent.com/kubeflow/kubeflow/${KUBEFLOW_TAG}/scripts/download.sh | bash

${KUBEFLOW_SRC}/scripts/kfctl.sh init ${KFAPP} --platform none
cd ${KFAPP}
${KUBEFLOW_SRC}/scripts/kfctl.sh generate k8s
${KUBEFLOW_SRC}/scripts/kfctl.sh apply k8s

# later we have to provide PV to all the available persistent volume claims
# if hostPath PV are used the we need to set the file permissions to allow the pods to write
# also need to check if the CoreDNS functionality is working or not
