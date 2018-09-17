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
	"_id": ObjectId("5b8e92158343ce0007746527"),
	"user_id": "Jeremy",
	"created_at": "2018-09-04 14:09:24",
	"from": {
		"address": "paris",
		"coordinates": {
			"lat": 48.85881005,
			"long": 2.32003101155031
		}
	},
	"to": {
		"address": "5 rue joseph riviere courbevoie",
		"coordinates": {
			"lat": 48.9023284,
			"long": 2.2562724
		}
	},
	"iteration": {
		"todo": 13,
		"done": 2
	},
	"status": "pending",
	"seat_count": 2,
	"prices": {
		"uber": {
			"Pool": [{
					"iteration": 0,
					"created_at": "2018-09-04 16:09:33",
					"low": 24,
					"high": 31,
					"average": 27.5,
					"min": 27.5,
					"max": 27.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				},
				{
					"iteration": 1,
					"created_at": "2018-09-04 16:09:42",
					"low": 24,
					"high": 31,
					"average": 27.5,
					"min": 27.5,
					"max": 27.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				}
			],
			"UberX": [{
					"iteration": 0,
					"created_at": "2018-09-04 16:09:33",
					"low": 29,
					"high": 36,
					"average": 32.5,
					"min": 32.5,
					"max": 32.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				},
				{
					"iteration": 1,
					"created_at": "2018-09-04 16:09:42",
					"low": 29,
					"high": 36,
					"average": 32.5,
					"min": 32.5,
					"max": 32.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				}
			],
			"Green": [{
					"iteration": 0,
					"created_at": "2018-09-04 16:09:33",
					"low": 29,
					"high": 36,
					"average": 32.5,
					"min": 32.5,
					"max": 32.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				},
				{
					"iteration": 1,
					"created_at": "2018-09-04 16:09:42",
					"low": 29,
					"high": 36,
					"average": 32.5,
					"min": 32.5,
					"max": 32.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				}
			],
			"Van": [{
					"iteration": 0,
					"created_at": "2018-09-04 16:09:33",
					"low": 31,
					"high": 39,
					"average": 35.0,
					"min": 35.0,
					"max": 35.0,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				},
				{
					"iteration": 1,
					"created_at": "2018-09-04 16:09:42",
					"low": 31,
					"high": 39,
					"average": 35.0,
					"min": 35.0,
					"max": 35.0,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				}
			],
			"ACCESS": [{
					"iteration": 0,
					"created_at": "2018-09-04 16:09:33",
					"low": 29,
					"high": 36,
					"average": 32.5,
					"min": 32.5,
					"max": 32.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				},
				{
					"iteration": 1,
					"created_at": "2018-09-04 16:09:42",
					"low": 29,
					"high": 36,
					"average": 32.5,
					"min": 32.5,
					"max": 32.5,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				}
			],
			"Berline": [{
					"iteration": 0,
					"created_at": "2018-09-04 16:09:33",
					"low": 31,
					"high": 39,
					"average": 35.0,
					"min": 35.0,
					"max": 35.0,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				},
				{
					"iteration": 1,
					"created_at": "2018-09-04 16:09:42",
					"low": 31,
					"high": 39,
					"average": 35.0,
					"min": 35.0,
					"max": 35.0,
					"dynamic_trend": 0.0,
					"global_trend": 0.0
				}
			]
		}
	}
}
```
