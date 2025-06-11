
docker build \
  --build-arg GROUPID=$(id -g) \
  --build-arg USERID=$(id -u) \
  --build-arg USERNAME=$USER \
  -f Dockerfile \
  -t pangyuteng/matlab:ptvreg-base .

docker push pangyuteng/matlab:ptvreg-base

docker build \
  --build-arg GROUPID=$(id -g) \
  --build-arg USERID=$(id -u) \
  --build-arg USERNAME=$USER \
  -f Dockerfile.prod \
  -t pangyuteng/matlab:ptvreg-prod .

docker push pangyuteng/matlab:ptvreg-prod