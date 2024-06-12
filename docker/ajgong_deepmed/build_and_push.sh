docker build --build-arg="TF_TAG=1.15.0-gpu-py3" -t pangyuteng/ajgong_deep_med_custom_pd:tf1.15 .
docker push pangyuteng/ajgong_deep_med_custom_pd:tf1.15
docker tag pangyuteng/ajgong_deep_med_custom_pd:tf1.15 pangyuteng/ajgong_deep_med_custom_pd:latest
docker push pangyuteng/ajgong_deep_med_custom_pd:latest