## Info

*"Com napisał... Napisałem"*

------------------------------------------------------------------------------------------------
**GeoToLocal_v2.py**

Poprawiona wersja poprzednika, cały kod przepisany jest do jednej funkcji, ponadto sam wylicza "lokalny promień Ziemi" na podstawie podanych szerokości.
Z danych geodezyjnych - można mu podać dokładne dane dla promienia na biegunie i równiku.
W kwestii matematycznej - jeszcze szukam informacji, czy da się dokładniej wyliczać wartości (może inna biblioteka i/lub inny wzór)

**geoToLocal.py**

Zamienia współrzędne geograficzne na lokalny układ współrzędnych, pewnie trzeba zrobić poprawki

**move_turtle.srv / moveTurtle_client.py / moveTurtle.server.py**

To miał być serwis do ROSa, by jakoś zaprogramować ruch roomby/żółwia, a potem domyślnie drona

Tylko jakiś błąd mi w ROSie wywala i nie wiem co z tym zrobić
