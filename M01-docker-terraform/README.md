# Docker Fundamentals

- Docker is like a portable house for storing and keeping essitials only associated within it.
To run docker, we use the command `docker run <DOCKER FILE NAME>`. To be able to interact with the docker file we run in `-it`as in `docker run -it <DOCKER FILE NAME>`, e.g. 
```bash 
docker run -it ubuntu
```

- Docker is stateless, which means after running a file any new activity created within it is not actively saved when you return into the container. Run `docker ps -aq` to see the list of created docker volumes (id) and `docker ps -a` to see the list of docker images. To remove all existing volumes (images), run `ddocker rm 'docker ps -aq'`
