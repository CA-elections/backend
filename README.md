# backend
[![forthebadge](https://forthebadge.com/images/badges/designed-in-ms-paint.svg)](https://forthebadge.com)


## instrukce

1. V souboru `db.ini` je nutné upravit parametr `Server` na správnou IP adresu/doménu
2. V souboru ˙bakalari_reader` je potřeba zadat správné přihlašovací údaje pro databázi
3. V Dockerfilu je potřeba změnit heslo uživatele, `User.objects.create_superuser(... 'user')` **->** `User.objects.create_superuser(... 'nove_heslo')`
4. Projekt se spustí pomocí `./rundocker` a běží na portu 8000, viz `Dockerfile`
