
#### compile pTVReg with `Matlab mcc` and build container for pTVReg execution for HTCondor

+ clone pTVReg in this folder

```

cd htcondor/matlab-mcc
git clone https://github.com/visva89/pTVreg.git

```

+ you will need to tweak 2 files in pTVreg

  + `mutils/My/image_metrics/metric_ngf.m`

  ```
  -   elseif Nd = 2;
  +   elseif Nd == 2;
  ```

  + `mutils/My/minFunc_2012_mod/autoDif/autoTensor.m`

  ```
  -        [~ ~ diff(:,:,j)] = funObj(x + mu*e_j,varargin{:});
  +        [junk1 junk2 diff(:,:,j)] = funObj(x + mu*e_j,varargin{:});
  ```

+ download test data to `workdir`

```
cd workdir
wget https://github.com/neurolabusc/niivue-images/raw/refs/heads/main/chris_t1.nii.gz
wget https://github.com/neurolabusc/niivue-images/raw/refs/heads/main/chris_t2.nii.gz
```

+ launch matlab, enter matlab credentials.

```

# CD TO THIS DIRECTORY
cd htcondor/matlab-mcc

# launch matlab in container in terminal mode
docker run --init -it --rm --shm-size=512M \
  -v $PWD:/opt/myapp \
  pangyuteng/matlab:ptvreg-base \
  bash

# important to goto this directory, then launch matlab??
cd /opt/myapp/

bash /bin/run.sh

# running below, then do the mcc step! executable file size needs to 
run('/opt/myapp/hola.m');
run('/opt/myapp/hola_cli.m');

```

+ compile entrypoint and dependencies with mcc

```
# above `run(..)` is crucial, or else file size fgor `~/Documents/MATLAB/hola_cli` is < 200KB, it should be ~ 1.2MB

mcc -v -R -nodisplay -R -singleCompThread -m /opt/myapp/hola_cli.m -a /opt/myapp/pTVreg/*

```

+ in seperate terminal head in to same container and test the compiled executable
  and confirm input args, generate output file is "good".

```

docker exec -it ...

cd ~/Documents/MATLAB

# optional - remove all prior files in `~/Documents/MATLAB`, keep it clean

rm /opt/myapp/workdir/output.nii.gz

bash run_hola_cli.sh /opt/matlab/R2024a \
  /opt/myapp/workdir/chris_t1.nii.gz \
  /opt/myapp/workdir/chris_t2.nii.gz \
  /opt/myapp/workdir/output.nii.gz

```

+ in running container, move executables to code repo `bin` folder, ensure `hola_cli` is a git LFS (this should was already set via `.gitattributes` file)

```

cd ~/Documents/MATLAB
cp hola_cli /opt/myapp/bin
cp run_hola_cli.sh /opt/myapp/bin

```

+ build "production container"

```
bash build_and_push.sh
```

+ test out binary

```

cd workdir

docker run --init -it --rm --shm-size=512M \
  -v $PWD:/workdir -w /workdir \
  pangyuteng/matlab:ptvreg-prod \
  bash

rm output.nii.gz
bash /opt/myapp/bin/run_hola_cli.sh /opt/matlab/R2024a chris_t1.nii.gz chris_t2.nii.gz output.nii.gz


```





## old notes

friday mcc funday

https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki?p=HowToRunMatlab

https://wiki.orc.gmu.edu/mkdocs/How_to_Compile_MATLAB_on_Hopper

https://github.com/visva89/pTVreg

https://github.com/visva89/pTVreg.git

git clone https://github.com/visva89/pTVreg.git

https://stackoverflow.com/questions/79108886/how-to-run-compiled-matlab-executable-without-matlab-installed

https://www-auth.cs.wisc.edu/lists/htcondor-users/htdig/search.shtml#gsc.tab=0&gsc.q=matlab%20mcc&gsc.sort=date

```

docker run --init -it -u $(id -u):$(id -g) --rm -p 5901:5901 -p 8888:8888 --shm-size=512M pangyuteng/matlab:ptvreg-base /bin/run.sh -browser

https://stackoverflow.com/questions/6657005/matlab-running-an-m-file-from-command-line
"C:\<a long path here>\matlab.exe" -nodisplay -nosplash -nodesktop -r "run('C:\<a long path here>\mfile.m'); exit;"


docker run --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M pangyuteng/matlab:ptvreg-base  -nodisplay -nosplash -nodesktop -r "run('/home/pteng/foobar.m'); exit;"

above actually worked... but it asks for credentials


docker run --init -it -u $(id -u):$(id -g) --rm -p 5901:5901 -p 8888:8888 --shm-size=512M pangyuteng/matlab:ptvreg-base -browser

above  perm denied

docker run --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M pangyuteng/matlab:ptvreg-base -browser

^^^ access gui via browser

mkdir workdir

docker run -v $PWD/workdir:/workdir \
  --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M pangyuteng/matlab:ptvreg-base bash

bash /bin/run.sh
^^^ terminal

mcc -v -R -nodisplay -R -singleCompThread -m /home/pteng/foobar.m

docker exec -it $running-container bash
cd ~/Documents/MATLAB

bash run_foobar.sh /opt/matlab/R2024a

+ exit container, rebuild container replace to have null entrypoint: `ENTRYPOINT [""]`

docker run --init -it --rm -p 5901:5901 -p 8888:8888 --shm-size=512M \
    -v $PWD/workdir:/workdir -w /workdir \
    pangyuteng/matlab:ptvreg-base bash /workdir/MATLAB/run_foobar.sh /opt/matlab/R2024a



+ testing/development
https://github.com/neurolabusc/niivue-images

cd workdir
wget https://github.com/neurolabusc/niivue-images/raw/refs/heads/main/chris_t1.nii.gz
wget https://github.com/neurolabusc/niivue-images/raw/refs/heads/main/chris_t2.nii.gz

cp hola.m workdir

docker run --init -it --rm --shm-size=512M \
  -v $PWD:/opt/myapp \
  pangyuteng/matlab:ptvreg bash

bash /bin/run.sh

run('/opt/myapp/foo.m');
run('/opt/myapp/foobar.m');
mcc -v -R -nodisplay -R -singleCompThread -m /opt/myapp/foobar.m

docker exec -it ...
cd ~/Documents/MATLAB
bash run_foobar.sh /opt/matlab/R2024a 123 abc


run('/opt/myapp/hola.m');

https://www.mathworks.com/matlabcentral/answers/355248-how-to-add-different-folders-while-generating-standalone-exe-using-mcc-command

mcc -v -R -nodisplay -R -singleCompThread -m /opt/myapp/hola_mcc.m -a /opt/myapp/pTVreg/*
bash run_hola_mcc.sh /opt/matlab/R2024a

mcc -v -R -nodisplay -R -singleCompThread -m /opt/myapp/hola_cli.m -a /opt/myapp/pTVreg/*

docker exec -it ...
cd ~/Documents/MATLAB
bash run_hola_mcc.sh /opt/matlab/R2024a 

bash run_hola_cli.sh /opt/matlab/R2024a \
  /opt/myapp/workdir/chris_t1.nii.gz \
  /opt/myapp/workdir/chris_t2.nii.gz \
  /opt/myapp/workdir/ok.nii.gz

cd ~/Documents/MATLAB
cp hola_cli /opt/myapp/bin
cp run_hola_cli.sh /opt/myapp/bin

bash build_and_push.sh

docker run -it --shm-size=512M -v $PWD/workdir:/workdir -w /workdir pangyuteng/matlab:ptvreg-prod bash

bash /opt/myapp/bin/run_hola_cli.sh /opt/matlab/R2024a \
  /workdir/chris_t1.nii.gz \
  /workdir/chris_t2.nii.gz \
  /workdir/ok.nii.gz


```