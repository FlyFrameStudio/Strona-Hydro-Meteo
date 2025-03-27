import os

# Ścieżki folderów
folder_wejscie = r"C:\Users\latmi\OneDrive\Pulpit\uczelnia\Dane_Hydrologiczne_IMGW\Przepływy_dobowe_XXX_lecie_1992_2021\polaczony TXT"
folder_wyjscie = r"C:\Users\latmi\OneDrive\Pulpit\uczelnia\Dane_Hydrologiczne_IMGW\Przepływy_dobowe_XXX_lecie_1992_2021\filtrowane TXT"
plik_wejscie = os.path.join(folder_wejscie, "polaczony.txt")
plik_wyjscie = os.path.join(folder_wyjscie, "filtrowane.txt")

# Upewnij się, że folder wyjściowy istnieje
os.makedirs(folder_wyjscie, exist_ok=True)

# Sprawdzenie poprawności odczytu pliku
if not os.path.exists(plik_wejscie):
    print("Niepoprawnie odczytano polaczony.txt")
    exit()
else:
    print("Poprawnie odczytano polaczony.txt")

# Pobranie danych od użytkownika
nazwa_stacji = input("Podaj nazwę stacji: ").strip()
rok_od = int(input("Podaj rok hydrologiczny od: "))
rok_do = int(input("Podaj rok hydrologiczny do: "))

print(f"Filtracja dla stacji: {nazwa_stacji}, od roku: {rok_od}, do roku: {rok_do}")

# Przetwarzanie pliku wejściowego
znalezione_dane = []
wszystkie_lata = set(range(rok_od, rok_do + 1))
znalezione_lata = set()
odnaleziono_stacje = False

with open(plik_wejscie, "r", encoding="utf-8") as plik:
    naglowek = plik.readline()  # Pominięcie nagłówka
    for linia in plik:
        dane = linia.strip().split(",")
        if len(dane) >= 10:
            nazwa = dane[1].strip()
            try:
                rok = int(dane[3].strip())
            except ValueError:
                continue  # Pomijanie błędnych danych
            
            if nazwa == nazwa_stacji:
                odnaleziono_stacje = True
            
            if nazwa == nazwa_stacji and rok_od <= rok <= rok_do:
                znalezione_dane.append(linia)
                znalezione_lata.add(rok)

brakujace_lata = wszystkie_lata - znalezione_lata

# Obsługa wyników
if not odnaleziono_stacje:
    print(f"Brak danych dla podanej stacji: {nazwa_stacji}")
    exit()

if znalezione_dane:
    with open(plik_wyjscie, "w", encoding="utf-8") as plik_wyj:
        plik_wyj.writelines(znalezione_dane)
    
    if brakujace_lata:
        pierwsze_dostepne = min(znalezione_lata) if znalezione_lata else rok_od
        ostatnie_dostepne = max(znalezione_lata) if znalezione_lata else rok_do
        print(f"Brak danych dla lat: {sorted(brakujace_lata)}, wyfiltrowano dla {pierwsze_dostepne} do {ostatnie_dostepne}")
    else:
        print("Poprawnie wyfiltrowano dane")
else:
    print("Brak danych w wybranym zakresie lat")