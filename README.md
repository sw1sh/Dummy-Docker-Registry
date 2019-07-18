Build
```
docker build . --tag dummy_registry
```

Run
```
docker run --rm -it -p 5000:5000 --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock dummy_registry
```
