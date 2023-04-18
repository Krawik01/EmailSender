import smtplib
from email.mime.text import MIMEText

class Student:
    def __init__(self, email, imie, nazwisko, punkty, ocena='', status=''):
        self.email = email
        self.imie = imie
        self.nazwisko = nazwisko
        self.punkty = punkty
        self.ocena = ocena
        self.status = status

    def __str__(self):
        return f"{self.email}, {self.imie} {self.nazwisko}, Punkty: {self.punkty}, Ocena: {self.ocena}, Status: {self.status}"


def wczytaj_dane_z_pliku(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            studenty = []
            for line in plik:
                dane = line.strip().split(',')
                if len(dane) == 6:
                    student = Student(dane[0], dane[1], dane[2], int(dane[3]), dane[4], dane[5])
                else:
                    student = Student(dane[0], dane[1], dane[2], int(dane[3]))
                studenty.append(student)
            return studenty
    except FileNotFoundError:
        print("Nie znaleziono pliku. Tworzenie nowego pliku.")
        return []


def zapisz_dane_do_pliku(nazwa_pliku, studenty):
    with open(nazwa_pliku, 'w') as plik:
        for student in studenty:
            plik.write(f"{student.email},{student.imie},{student.nazwisko},{student.punkty},{student.ocena},{student.status}\n")


def wystaw_ocene(studenty, punkty_do_oceny):
    for student in studenty:
        if student.status != 'GRADED' and student.status != 'MAILED':
            if student.punkty >= punkty_do_oceny:
                student.ocena = 'PASS'
            else:
                student.ocena = 'FAIL'
            student.status = 'GRADED'
    print("Automatycznie wystawiono oceny.")


def dodaj_studenta(studenty):
    email = input("Podaj email studenta: ")
    for student in studenty:
        if student.email == email:
            print("Student o podanym emailu już istnieje.")
            return

    imie = input("Podaj imię studenta: ")
    nazwisko = input("Podaj nazwisko studenta: ")
    punkty = int(input("Podaj liczbę uzyskanych punktów: "))

    student = Student(email, imie, nazwisko, punkty)
    studenty.append(student)
    print("Dodano nowego studenta.")


def usun_studenta(studenty):
    email = input("Podaj email studenta do usunięcia: ")
    for student in studenty:
        if student.email == email:
            studenty.remove(student)
            print("Usunięto studenta.")
            return

    print("Nie znaleziono studenta o podanym emailu.")

def aktualizuj_dane_studenta(studenty):
    email = input("Podaj email studenta do aktualizacji: ")
    for student in studenty:
        if student.email == email:
            imie = input(f"Aktualny email studenta: {student.email}. Podaj nowe imię studenta: ")
            nazwisko = input(f"Aktualne imię studenta: {student.imie}. Podaj nowe nazwisko studenta: ")
            punkty = input(f"Aktualne nazwisko studenta: {student.nazwisko}. Podaj nowe punkty studenta: ")

            student.imie = imie
            student.nazwisko = nazwisko
            student.punkty = punkty

            print("Zaktualizowano dane studenta.")
            return

    print("Nie znaleziono studenta o podanym emailu.")


def wyslij_emaile_do_wszystkich_studentow(studenty, subject, body, sender, password):
    for student in studenty:

        email = student["email"]

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email

        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, email, msg.as_string())
        smtp_server.quit()



punkty_do_oceny = 100

def main():
    studenty = []  # Lista przechowująca informacje o studentach

    while True:
        print("1. Dodaj studenta")
        print("2. Usuń studenta")
        print("3. Aktualizuj dane studenta")
        print("4. Wyślij emaile z ocenami")
        print("5. Zakończ program")
        wybor = input("Wybierz opcję (1/2/3/4/5): ")

        if wybor == "1":
            dodaj_studenta(studenty)
        elif wybor == "2":
            usun_studenta(studenty)
        elif wybor == "3":
            aktualizuj_dane_studenta(studenty)
        elif wybor == "4":
            subject = input("Przykładowy temat wiadomości")
            body = input("Przykładowa treść wiadomości")
            sender = input("moj.email@example.com")
            password = input("moje_haslo")

            # Wywołanie funkcji do wysłania wiadomości email do wszystkich studentów na liście
            wyslij_emaile_do_wszystkich_studentow(studenty, subject, body, sender, password)
        elif wybor == "5":
            print("Program został zakończony.")
            break
        else:
            print("Niepoprawny wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()