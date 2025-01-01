test etmek icin bu kodu gir:
curl.exe -X POST http://127.0.0.1:5000/api/scan -H "Authorization: 5c65ef982d9cc941a57ab387f855a1481f15ff76292b84beca231f395df84694"

waitress server baslatmak icin:
waitress-serve --port=5000 network_scan:app

gunicorn baslatma kodu:
gunicorn -w 4 -b 0.0.0.0:5000 network_scan:app
