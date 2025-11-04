scp -i aktoviz-keys.pem -r  app ubuntu@51.21.32.24:~/
scp -i aktoviz-keys.pem -r  app/Dockerfile ubuntu@51.21.32.24:~/app
scp -i aktoviz-keys.pem -r  app/requirements.txt ubuntu@51.21.32.24:~/app
scp -i aktoviz-keys.pem -r  app/docker-compose.yml ubuntu@51.21.32.24:~/
scp -i aktoviz-keys.pem -r  app/app.py ubuntu@51.21.32.24:~/app

