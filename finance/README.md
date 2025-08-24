## setup environment with docker, and run notebook

```

docker run -it --env TASTYTRADE_XXX --env TASTYTRADE_XXXX \
-v ${PWD}:/opt -w /opt -p 8888:8888 pangyuteng/tasty bash 
```

gpu
```

 --gpus device=0 

```
### convenience jupyter lab up with docker-compose

```
doocker-compose up --build
```




