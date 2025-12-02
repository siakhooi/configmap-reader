help:
clean:
	rm -rf dist target coverage \
	.coverage \
	src/configmap_reader/__pycache__ \
	tests/__pycache__ \
	.pytest_cache
run:
	poetry run configmap-reader
set-version:
	scripts/set-version.sh
build:
	poetry build
install:
	poetry install
flake8:
	poetry run flake8
update:
	poetry update
test:
	 poetry run pytest --capture=sys \
	 --junit-xml=coverage/test-results.xml \
	 --cov=configmap_reader \
	 --cov-report term-missing  \
	 --cov-report xml:coverage/coverage.xml \
	 --cov-report html:coverage/coverage.html \
	 --cov-report lcov:coverage/coverage.info

all: clean set-version install flake8 build test

release:
	scripts/release.sh

commit:
	scripts/git-commit.sh
	git push




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

