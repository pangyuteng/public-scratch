
friday mcc funday

https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki?p=HowToRunMatlab

https://wiki.orc.gmu.edu/mkdocs/How_to_Compile_MATLAB_on_Hopper

https://github.com/visva89/pTVreg

https://github.com/visva89/pTVreg.git

git clone https://github.com/visva89/pTVreg.git

https://stackoverflow.com/questions/79108886/how-to-run-compiled-matlab-executable-without-matlab-installed





docker run --init -it -u $(id -u):$(id -g) --rm -p 5901:5901 -p 8888:8888 --shm-size=512M $USER:matlab -browser

https://stackoverflow.com/questions/6657005/matlab-running-an-m-file-from-command-line
"C:\<a long path here>\matlab.exe" -nodisplay -nosplash -nodesktop -r "run('C:\<a long path here>\mfile.m'); exit;"

```
docker run --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M $USER:matlab  -nodisplay -nosplash -nodesktop -r "run('/home/pteng/foobar.m'); exit;"
```
above actually worked... but it asks for credentials

```
docker run --init -it -u $(id -u):$(id -g) --rm -p 5901:5901 -p 8888:8888 --shm-size=512M $USER:matlab -browser
```
above  perm denied

docker run --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M $USER:matlab -browser

^^^ access gui via browser

mkdir workdir
docker run -v $PWD/workdir:/workdir \
  --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M $USER:matlab sh

^^^ terminal

mcc -v -R -nodisplay -R -singleCompThread -m /home/pteng/foobar.m

docker exec -it $running-container bash
cd ~/Documents/MATLAB

bash run_foobar.sh /opt/matlab/R2024a

+ exit container, rebuild container replace to have null entrypoint: `ENTRYPOINT [""]`

docker run --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M \
    -v $PWD/workdir:/workdir -w /workdir \
    $USER:matlab bash /workdir/MATLAB/run_foobar.sh /opt/matlab/R2024a
    
