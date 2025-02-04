# Bazowy obraz
FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie wymaganych plików
COPY requirements.txt /app/

# Instalowanie zależności
RUN pip install -r requirements.txt

# Kopiowanie reszty aplikacji
COPY . /app/

# Otwieramy port 5000
EXPOSE 5000

# Uruchomienie aplikacji
CMD ["flask", "run", "--host=0.0.0.0"]
