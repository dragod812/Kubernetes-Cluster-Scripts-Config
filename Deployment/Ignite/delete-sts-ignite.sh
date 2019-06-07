kubectl delete sts ignite
kubectl delete pvc $(kubectl get pvc | grep ignite | awk '{print $1}')
kubectl delete pv $(kubectl get pv | grep ignite | awk '{print $1}')
kubectl delete service ignite
