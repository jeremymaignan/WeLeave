curl -H "Content-Type: application/json" -X POST -d '{
"from": "paris",
"to": "5 rue joseph riviere courbevoie",
"number_seat": 2,
"user_id": "Jeremy"
}'   http://0.0.0.0:5000/uber &&
echo "\nDone" ;
curl -H "Content-Type: application/json" -X POST -d '{
"from": "orly",
"to": "5 rue joseph riviere courbevoie",
"number_seat": 2,
"user_id": "Steven"
}'   http://0.0.0.0:5000/uber && 
echo "\nDone" ;
curl -H "Content-Type: application/json" -X POST -d '{
"from": "versailles",
"to": "5 rue joseph riviere courbevoie",
"number_seat": 2,
"user_id": "Mehdi"
}'   http://0.0.0.0:5000/uber &&
echo "\nDone" ;