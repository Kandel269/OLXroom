Program ma za zadanie śledzenia umieszczanych nowych ogłoszeń mieszkań na stronie www.olx.pl i informować o tym użytkownika. Program pozwala na dokonywanie filtracji preferowanych mieszkań np. maksymalna kwota miesięcznego najmu. Program skanuje co 15 min wyżej wymienioną stronę i gdy znajdzie nowe ogłoszenie spełniające kryteria, to wyświetla stosowną informację w oknie programu.

Istnieje możliwość rozbudowania programu o informowanie drogą e-mailową czy też smsową.

Uruchomienie:
-
1. Pobierz aplikację i załącz ją
2. Wpisz w odpowiednią rubrykę preferowane miasto - warunek konieczny (pamiętaj o polskich znakach)
3. dodaj opcjonalne filtry
4. Naciśnij przycisk "Start"

UWAGA:
-
Upewnij się, że masz dobrze ustawiony czas systemowy, program z niego korzysta.

Dane godzinowe pobierane ze strony olx mają różnice dwóch godzin. Np. jeżeli na stronie
widnieje godzina dodania lokalu 14:00 to program wykrywa to jako 12:00. Dlatego program wprowadza 2h korektę. Możliwe
iż taka sytuacja zachodzi tylko i wyłącznie na moim urządzeniu (program nie był testowany na innych urządzeniach), więc istnieje możliwość, że 
program nie będzie działał u kogoś innego poprawnie. W przyszłości mam zamiar usprawnić działanie programu, aby obejść tego typu problem.

Główne biblioteki:
- PyQt6
- BeautifulSoup