docker build \
  --build-arg GROUPID=$(id -g) \
  --build-arg USERID=$(id -u) \
  --build-arg USERNAME=$USER \
  -t $USER:matlab .
