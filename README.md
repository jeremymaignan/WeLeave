# WeLeave

## Purpose:

Real time cab fare analytics.

Supported apps:
- Uber
- Marcel
- SnapCar
- Drive
- Taxi G7
- Hi Cab
- Allocab
- Felix


![output_screenshot](https://github.com/jeremymaignan/uber-fare-trend-analytics/blob/master/screenshot.png)

## API:

### Run API & DB

```sh
docker-compose up --build
```
Mongo is now live: localhost:27017

### Create ride: 
```sh
$curl -H "Content-Type: application/json" -X POST -d @payload.json http://0.0.0.0:5000/weleave
```
```json
{
  "id": "5b86b84981973b00073a3110"
}
```
### Extend job: 
```sh
$curl -H "Content-Type: application/json"  -X PATCH -d '{"iteration": 10}'  http://0.0.0.0:5000/weleave/5b86b84981973b00073a3110
```

### Get ride prices: 
```sh
$curl -H "Content-Type: application/json" -X GET http://0.0.0.0:5000/weleave/5b86b84981973b00073a3110
```
```json
{
	"_id": "5b86b84981973b00073a3110",
	"user_id": "jeremymaignan",
	"created_at": "2018-08-29 15:14:17",
	"start_at": "2018-08-29 15:12:17",
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
$curl -H "Content-Type: application/json" -X DELETE  http://0.0.0.0:5000/weleave/5b86b84981973b00073a3110
```

## Database schema:
```json
{
    "_id" : ObjectId("5b9f7aa020a37a000afc5d09"),
    "user_id" : "Jeremy",
    "created_at" : "2018-09-17 09:57:52",
    "start_at" : "2018-09-13 21:40:18",
    "from" : {
        "address" : "6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris, France",
        "zip_code" : "75004",
        "coordinates" : {
            "lat" : 48.85293695,
            "long" : 2.35005149954546
        }
    },
    "to" : {
        "address" : "58 rue joseph riviere courbevoie",
        "zip_code" : "92400",
        "coordinates" : {
            "lat" : 48.9023284,
            "long" : 2.2562724
        }
    },
    "iteration" : {
        "todo" : 13,
        "done" : 2
    },
    "status" : "pending",
    "seat_count" : 1,
    "prices" : {
        "uber" : {
            "Berline" : [ 
                {
                    "price" : 41.5,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 09:58:03",
                    "iteration" : 0
                }, 
                {
                    "price" : 41.5,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 10:00:02",
                    "iteration" : 1
                }
            ],
            "Pool" : [ 
                {
                    "price" : 20.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 09:58:03",
                    "iteration" : 0
                }, 
                {
                    "price" : 20.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 10:00:02",
                    "iteration" : 1
                }
            ],
            "UberX" : [ 
                {
                    "price" : 24.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 09:58:03",
                    "iteration" : 0
                }, 
                {
                    "price" : 24.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 10:00:02",
                    "iteration" : 1
                }
            ],
            "Green" : [ 
                {
                    "price" : 24.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 09:58:03",
                    "iteration" : 0
                }, 
                {
                    "price" : 24.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 10:00:02",
                    "iteration" : 1
                }
            ],
            "Van" : [ 
                {
                    "price" : 41.5,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 09:58:03",
                    "iteration" : 0
                }, 
                {
                    "price" : 41.5,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 10:00:02",
                    "iteration" : 1
                }
            ],
            "ACCESS" : [ 
                {
                    "price" : 24.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 09:58:03",
                    "iteration" : 0
                }, 
                {
                    "price" : 24.0,
                    "distance" : 7.2,
                    "duration" : 29.0,
                    "created_at" : "2018-09-17 10:00:02",
                    "iteration" : 1
                }
            ]
        },
        "marcel" : {
            "Berline" : [ 
                {
                    "price" : 25.0,
                    "distance" : 11.386,
                    "duration" : 34,
                    "created_at" : "2018-09-17 09:58:04",
                    "iteration" : 0
                }, 
                {
                    "price" : 25.3,
                    "distance" : 11.386,
                    "duration" : 35,
                    "created_at" : "2018-09-17 10:00:03",
                    "iteration" : 1
                }
            ],
            "Business" : [ 
                {
                    "price" : 37.0,
                    "distance" : 11.386,
                    "duration" : 34,
                    "created_at" : "2018-09-17 09:58:06",
                    "iteration" : 0
                }, 
                {
                    "price" : 37.3,
                    "distance" : 11.386,
                    "duration" : 35,
                    "created_at" : "2018-09-17 10:00:06",
                    "iteration" : 1
                }
            ],
            "Van" : [ 
                {
                    "price" : 40.3,
                    "distance" : 11.386,
                    "duration" : 34,
                    "created_at" : "2018-09-17 09:58:07",
                    "iteration" : 0
                }, 
                {
                    "price" : 40.6,
                    "distance" : 11.386,
                    "duration" : 35,
                    "created_at" : "2018-09-17 10:00:07",
                    "iteration" : 1
                }
            ],
            "moto" : [ 
                {
                    "price" : 60.0,
                    "distance" : 11.192,
                    "duration" : 27,
                    "created_at" : "2018-09-17 09:58:08",
                    "iteration" : 0
                }, 
                {
                    "price" : 60.0,
                    "distance" : 11.192,
                    "duration" : 27,
                    "created_at" : "2018-09-17 10:00:07",
                    "iteration" : 1
                }
            ]
        },
        "snapcar" : {
            "executive" : [ 
                {
                    "price" : 33,
                    "created_at" : "2018-09-17 09:58:09",
                    "iteration" : 0
                }, 
                {
                    "price" : 33,
                    "created_at" : "2018-09-17 10:00:08",
                    "iteration" : 1
                }
            ],
            "classic" : [ 
                {
                    "price" : 26,
                    "created_at" : "2018-09-17 09:58:09",
                    "iteration" : 0
                }, 
                {
                    "price" : 26,
                    "created_at" : "2018-09-17 10:00:08",
                    "iteration" : 1
                }
            ],
            "van" : [ 
                {
                    "price" : 35,
                    "created_at" : "2018-09-17 09:58:09",
                    "iteration" : 0
                }, 
                {
                    "price" : 35,
                    "created_at" : "2018-09-17 10:00:08",
                    "iteration" : 1
                }
            ]
        },
        "allocab" : {
            "Berline classe affaires" : [ 
                {
                    "price" : 41.3,
                    "created_at" : "2018-09-17 09:58:15",
                    "iteration" : 0
                }
            ],
            "Van classe éco" : [ 
                {
                    "price" : 37.17,
                    "created_at" : "2018-09-17 09:58:15",
                    "iteration" : 0
                }, 
                {
                    "price" : 37.76,
                    "created_at" : "2018-09-17 10:00:31",
                    "iteration" : 1
                }
            ],
            "Berline classe éco" : [ 
                {
                    "price" : 29.5,
                    "created_at" : "2018-09-17 09:58:15",
                    "iteration" : 0
                }, 
                {
                    "price" : 29.99,
                    "created_at" : "2018-09-17 10:00:31",
                    "iteration" : 1
                }
            ]
        },
        "g7" : {},
        "drive" : {
            "Premium" : [ 
                {
                    "price" : 32,
                    "distance" : 8.8,
                    "duration" : 30,
                    "created_at" : "2018-09-17 09:58:16",
                    "iteration" : 0
                }, 
                {
                    "price" : 32,
                    "distance" : 8.8,
                    "duration" : 30,
                    "created_at" : "2018-09-17 10:00:32",
                    "iteration" : 1
                }
            ],
            "Van" : [ 
                {
                    "price" : 32,
                    "distance" : 8.8,
                    "duration" : 30,
                    "created_at" : "2018-09-17 09:58:17",
                    "iteration" : 0
                }, 
                {
                    "price" : 32,
                    "distance" : 8.8,
                    "duration" : 30,
                    "created_at" : "2018-09-17 10:00:32",
                    "iteration" : 1
                }
            ]
        },
        "hicab" : {
            "Moto" : [ 
                {
                    "distance" : 11.192,
                    "duration" : 31,
                    "price" : 60.0,
                    "created_at" : "2018-09-17 09:58:18",
                    "iteration" : 0
                }, 
                {
                    "distance" : 11.192,
                    "duration" : 32,
                    "price" : 60.0,
                    "created_at" : "2018-09-17 10:00:33",
                    "iteration" : 1
                }
            ],
            "Scooter" : [ 
                {
                    "distance" : 11.192,
                    "duration" : 31,
                    "price" : 45.0,
                    "created_at" : "2018-09-17 09:58:19",
                    "iteration" : 0
                }, 
                {
                    "distance" : 11.192,
                    "duration" : 32,
                    "price" : 45.0,
                    "created_at" : "2018-09-17 10:00:34",
                    "iteration" : 1
                }
            ],
            "E-Scooter" : [ 
                {
                    "distance" : 11.192,
                    "duration" : 31,
                    "price" : 31.0,
                    "created_at" : "2018-09-17 09:58:19",
                    "iteration" : 0
                }, 
                {
                    "distance" : 11.192,
                    "duration" : 32,
                    "price" : 31.0,
                    "created_at" : "2018-09-17 10:00:34",
                    "iteration" : 1
                }
            ],
            "Berline" : [ 
                {
                    "distance" : 11.386,
                    "duration" : 34,
                    "price" : 36.0,
                    "created_at" : "2018-09-17 09:58:20",
                    "iteration" : 0
                }, 
                {
                    "distance" : 11.386,
                    "duration" : 35,
                    "price" : 36.0,
                    "created_at" : "2018-09-17 10:00:35",
                    "iteration" : 1
                }
            ],
            "Van" : [ 
                {
                    "distance" : 11.386,
                    "duration" : 34,
                    "price" : 57.0,
                    "created_at" : "2018-09-17 09:58:20",
                    "iteration" : 0
                }, 
                {
                    "distance" : 11.386,
                    "duration" : 35,
                    "price" : 58.0,
                    "created_at" : "2018-09-17 10:00:36",
                    "iteration" : 1
                }
            ]
        }
    }
}
```
