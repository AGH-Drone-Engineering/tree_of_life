Całość rozwiązania

Sekcje:
READ: Wczytywanie z bazy
FIND SHORTEST: Znajdowanie najkrótszej ścieżki (DrawRealMap3() rysuje znalezioną najkrótszą ścieżkę)
TRAVEL: Wyświetlanie drogi do przebycia (droga też zwracana jest jako zbiór punktów i wyświetlana na ekranie)

W pliku pid.py w fragmencie:
################ UNCOMMENT THIS TO SEE EVERY STEP #################
można odkomentować kod aby wyświetlać podróż od punktu do punktu.

Głównym plikiem jest Read_FindShortest_Travel.py, inne są pomocnicze.



Sekcje do których należą pliki:

***GŁÓWNY PLIK:
Read_FindShortest_Travel.py

***READ (and database connection):
dodaj_moje_punkty.py
pobierz_punkty_z_bazy_do_listy.py
usuń_punkt.py
key.json

***FIND SHORTEST: 
PuLP.py

***TRAVEL:
pid.py

***INNE:
config.py
help_functions.py
pure_map_dark.png

***INNE NIEUŻYWANE:
README.txt
pid_copy.py
tree_points.csv



*pliki są zależne od siebie, więc aby działały powinny być w jednym folderze

*czasem jest problem z wczytywaniem pliku np. png, wtedy trzeba dodać ścieżkę mypath (która jest zdefiniowana w pliku config.py)
###########
mypath:str=str(os.path.dirname(__file__))+"\\"
###########

w następujący sposób:
###########
import config
config.mypath+"my_file_name.png"
###########

