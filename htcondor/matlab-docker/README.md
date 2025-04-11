



https://www.mathworks.com/help/cloudcenter/ug/matlab-container-on-docker-hub.html

docker run --init -it --rm -p 5901:5901 -p 6080:6080 --shm-size=512M mathworks/matlab:r2024a -vnc



https://www.mathworks.com/help/cloudcenter/ug/create-a-custom-matlab-container.html

RUN useradd -ms /bin/bash <USERNAME>



bash build.sh
bash start.sh


## TODO:  how do you compile matlab cli ? to use without license???
