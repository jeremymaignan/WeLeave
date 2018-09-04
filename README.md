# Uber Fare Trend Analytics

## Run API & DB

```sh
docker-compose up --build
```
Mongo is now live: localhost:27017

## API:

### Create ride: 
```sh
$curl -H "Content-Type: application/json" -X POST -d @payload.json http://0.0.0.0:5000/uber
```
```json
{
  "id": "5b86b84981973b00073a3110"
}
```
### Extend job: 
```sh
$curl -H "Content-Type: application/json"  -X PATCH -d '{"iteration": 10}'  http://0.0.0.0:5000/uber/5b86b84981973b00073a3110
```

### Get ride prices: 
```sh
$curl -H "Content-Type: application/json" -X GET http://0.0.0.0:5000/uber/5b86b84981973b00073a3110
```
```json
{
	"_id": "5b86b84981973b00073a3110",
	"user_id": "jeremymaignan",
	"created_at": "2018-08-29 15:14:17",
	"from": {
		"address": "paris",
		"coordinates": {
			"lat": 48.85881005,
			"long": 2.32003101155031
		}
	},
	"to": {
		"address": "orly",
		"coordinates": {
			"lat": 48.7431683,
			"long": 2.402391
		}
	},
	"iteration": 15,
	"status": "pending",
	"seat_count": 2,
	"prices": {}
}
```

### Stop ride:
```sh
$curl -H "Content-Type: application/json" -X DELETE  http://0.0.0.0:5000/uber/5b86b84981973b00073a3110
```

## Database schema:
```json
{
    "_id" : "5b86b3045b274300071bbaa7",
    "user_id" : "jeremymaignan",
    "created_at" : "2018-08-29 14:51:48",
    "from" : {
        "address" : "paris",
        "coordinates" : {
            "lat" : 48.85881005,
            "long" : 2.32003101155031
        }
    },
    "to" : {
        "address" : "orly",
        "coordinates" : {
            "lat" : 48.7431683,
            "long" : 2.402391
        }
    },
    "iteration" : 14,
    "status" : "stoped",
    "seat_count" : 2,
    "prices" : {
        "uber" : {
            "Pool" : [ 
                {
                    "iteration" : 0,
                    "created_at" : "2018-08-29 16:56:25",
                    "low" : 25,
                    "high" : 33,
                    "average" : 29.0
                }
            ],
            "UberX" : [ 
                {
                    "iteration" : 0,
                    "created_at" : "2018-08-29 16:56:25",
                    "low" : 30,
                    "high" : 38,
                    "average" : 34.0
                }
            ],
            "Green" : [ 
                {
                    "iteration" : 0,
                    "created_at" : "2018-08-29 16:56:25",
                    "low" : 30,
                    "high" : 38,
                    "average" : 34.0
                }
            ],
            "Van" : [ 
                {
                    "iteration" : 0,
                    "created_at" : "2018-08-29 16:56:25",
                    "low" : 50,
                    "high" : 62,
                    "average" : 56.0
                }
            ],
            "ACCESS" : [ 
                {
                    "iteration" : 0,
                    "created_at" : "2018-08-29 16:56:25",
                    "low" : 30,
                    "high" : 38,
                    "average" : 34.0
                }
            ],
            "Berline" : [ 
                {
                    "iteration" : 0,
                    "created_at" : "2018-08-29 16:56:25",
                    "low" : 50,
                    "high" : 62,
                    "average" : 56.0
                }
            ]
        }
    }
}
```
