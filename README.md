# Instagram-Scraper

Dit is een scraper voor het Instagram platform wat automatisch zoekt naar gespecificieerde termen in de stories van geselecteerde accounts.
Het is bedoeld als ondersteuning in realtime OSINT onderzoek bij bijvoorbeeld rellen, illegale feesten en andere gebeurtenissen met een tijdsdruk.

Dit programma is geschreven voor het vak ifosi van de opleiding Forensisch ICT bij de Hogeschool Leiden.

## Installatie
Het programma is ontworpen om op een server te draaien. Hiervoor is `docker` en `docker-compose` vereist.
Vervolgens kunnen de instellingen worden aangepast in het `config/config.json` bestand en kunnen de zoektermen in `config/buildingblocks` worden gezet.
Om het programma te starten, gebruik het volgende commando:
```bash
docker-compose up -d
```
Hierna is het programma beschikbaar op het IP-adres van de server en poort 5000. Deze poort kan worden aangepast door het `docker-compose.yml` bestand aan te passen.

## Operatie
Als het programma in de lucht is zal het ongeveer elke 5 minuten de stories van de geselecteerde gebruikers scannen.
Als er iets wordt gevonden zal de website de nieuwe afbeelding laten zien en een notificatie naar de gebruiker sturen.
Indien de afbeelding irrelevant is, kan deze worden gemarkeerd als een 'false-positive'. Hierna wordt de afbeelding verwijderd.
Als de afbeelding bewaard moet blijven, maar niet meer op de website te zien hoeven zijn kan deze worden verborgen.
De afbeelding is dan terug te vinden in de `data` folder.
Hieronder staat een screenshot van het programma in werking met voorbeeld data.

![Screenshot](/screenshot.png)
