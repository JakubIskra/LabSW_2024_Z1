# LabSW_2024_Z1
Rozwiązania do zadania 1

Polecenia niezbędne do:
a. zbudowania opracowanego obrazu kontenera
docker build -t server-app .

b. uruchomienia kontenera na podstawie zbudowanego obrazu
docker run -d -p 5000:5000 --name server-container server-app

c. sposobu uzyskania informacji, które wygenerował serwer w trakcie uruchamiania kontenera
docker logs server-container

d. sprawdzenia ile warstw posiada zbudowany obraz
docker history server-app
