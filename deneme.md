test etmek icin bu kodu gir:
curl.exe -X POST http://127.0.0.1:5000/api/scan -H "Authorization: api-address"

waitress server baslatmak icin:
waitress-serve --port=5000 network_scan:app

gunicorn baslatma kodu:
gunicorn -w 4 -b 0.0.0.0:5000 network_scan:app

once buradan yap sonra zaten serverlari linux tabanli yapicagin icin gunicorn yaparsin
ve sonra .env dosyasinida aktarirsin linuxe
