# consumption-notifier
 notifies lte consumption


docker build -t rphlct/consumption-notifier:latest . 

docker run --name consumption-notifier -d consumption-notifier

docker push rphlct/consumption-notifier:latest