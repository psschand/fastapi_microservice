
# clean docker setup 
  docker kill $(docker ps -q) # stop all containers
  docker rm $(docker ps -a -q) # remove all containers 
  docker rmi $(docker images -q) # remove all images
  docker network prune # remove all networks
  docker volume prune # remove all volumes 

# run backend service
docker-compose up

# test service at the below
localhost:8000/docs

# Test Data upload to DB
you can upload the election-test-data csv to the api

# yet to Implement
1-data validation
2-authentication
3-presenting data on UI