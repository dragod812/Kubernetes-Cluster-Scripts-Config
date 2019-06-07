kubectl create -f RBAC.xml
kubectl create -f ignite-stateful-set.yaml
kubectl exec -it ignite-0 /bin/bash
./apache-ignite/bin/control.sh --activate

# if running on an offline environment the kube persistence needs to be copied to the volume directory.
# the CONFIG_URI env variable needs to be changed to the volume mount path inside the docker( /data/ignite/kube-persistence.xml )
