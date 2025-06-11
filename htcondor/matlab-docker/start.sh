


docker run -u $(id -u):$(id -g) --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M $USER:matlab -browser


docker run --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M $USER:matlab -browser
