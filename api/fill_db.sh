date_now="`date +'%Y-%m-%d %H:%M:%S'`"
echo $date_now
curl -H "Content-Type: application/json" -X POST -d '{
"from": {"address": "6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris, France", "zip_code": "75004"},
"to":  {"address": "5 rue joseph riviere courbevoie", "zip_code": "92400"},
"number_seat": 1,
"user_id": "Jeremy",
"start_at": "2018-09-13 21:40:18"
}'   http://0.0.0.0:5000/uber &&
echo "\nDone" ;
curl -H "Content-Type: application/json" -X POST -d '{
"from": {"address": "aeorport orly sud", "zip_code": "94390"},
"to": {"address": "5 rue joseph riviere courbevoie", "zip_code": "92400"},
"number_seat": 2,
"user_id": "Steven",
"start_at": "2018-09-13 21:40:18"
}'   http://0.0.0.0:5000/uber && 
echo "\nDone" ;
curl -H "Content-Type: application/json" -X POST -d '{
"from": {"address": "versailles", "zip_code": "78000"},
"to": {"address": "5 rue joseph riviere courbevoie", "zip_code": "92400"},
"number_seat": 5,
"user_id": "Mehdi",
"start_at": "2018-09-13 21:40:18"
}'   http://0.0.0.0:5000/uber &&
echo "\nDone" ;
curl -H "Content-Type: application/json" -X POST -d '{
"from": {"address": "6 Parvis Notre-Dame - Pl. Jean-Paul II, 75004 Paris, France", "zip_code": "75004"},
"to":  {"address": "5 rue joseph riviere courbevoie", "zip_code": "92400"},
"number_seat": 6,
"user_id": "Jeremy",
"start_at": "2018-09-13 21:40:18"
}'   http://0.0.0.0:5000/uber &&
echo "\nDone" ;
curl -H "Content-Type: application/json" -X POST -d '{
"from": {"address": "aeorport orly sud", "zip_code": "94390"},
"to": {"address": "5 rue joseph riviere courbevoie", "zip_code": "92400"},
"number_seat": 7,
"user_id": "Steven",
"start_at": "2018-09-13 21:40:18"
}'   http://0.0.0.0:5000/uber && 
echo "\nDone" ;
curl -H "Content-Type: application/json" -X POST -d '{
"from": {"address": "versailles", "zip_code": "78000"},
"to": {"address": "5 rue joseph riviere courbevoie", "zip_code": "92400"},
"number_seat": 3,
"user_id": "Mehdi",
"start_at": "2018-09-13 21:40:18"
}'   http://0.0.0.0:5000/uber &&
echo "\nDone" ;