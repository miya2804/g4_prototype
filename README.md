# g4_prototype

## requirements
- Docker Engine
- curl(Optional)

## usage
### Running Container
```
docker-compose up
```
### Registering Room(Optional)
```
curl -X POST http://localhost:8080/room
```

### Registering Sensor(Optional)
```
curl -X POST http://localhost:8080/sensor
```

### Getting Sensor States(Optional)
```
curl http://localhost:8080
```
