# configmap-reader

microservice to read and return content of a configmap

## Build

```
docker build -t siakhooi/configmap-reader:latest .
docker push siakhooi/configmap-reader:latest
```

## Deploy to clusters

```
kubectl apply -f ./configmap-reader
```

## Use

### Port forwarding

```
kubectl port-forward svc/configmap-reader 8080:80
```

## Test

```bash
curl http://localhost:8080/config
```

- edit the configmap `configmap-reader-data` and call again will return latest value

## Deliverables

- https://hub.docker.com/r/siakhooi/configmap-reader
