# Etap 1: Budowanie zależności i aplikacji
FROM python:3.11-slim AS builder

# Informacje o autorze
LABEL maintainer="Jakub Iskra"

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalacja zależności aplikacji
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Etap 2: Budowanie minimalnego obrazu
FROM python:3.11-slim

# Informacje o autorze
LABEL maintainer="Jakub Iskra"

# Ustawienia środowiska
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Kopiowanie aplikacji i zależności
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY . .

# Otwieranie portu aplikacji
EXPOSE 5000

# HEALTHCHECK: Sprawdzanie stanu aplikacji
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000 || exit 1

# Uruchamianie aplikacji
CMD ["python", "zad1.py"]
