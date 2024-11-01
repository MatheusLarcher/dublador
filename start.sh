docker stop dublador
docker rm dublador
docker rmi dublador
docker build -t dublador .
docker run -d -p 8010:8010 --name dublador dublador