docker-build:
	cd docker && docker build -t siakhooi/configmap-reader:latest .
docker-push:
	docker push siakhooi/configmap-reader:latest
apply:
	shed-kubectl apply -f ./kubernetes
delete:
	shed-kubectl delete -f ./kubernetes
k8s-pf:
	shed-kubectl port-forward svc/configmap-reader 8080:80

curl:
	curl -i http://localhost:8080/config

health:
	curl -i http://localhost:8080/health


k3d-up:
	k3d-up
import:
	k3d-image-import  siakhooi/configmap-reader:latest
k3d-down:
	k3d-down
