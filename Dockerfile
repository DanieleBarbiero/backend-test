# Usa un’immagine base Python alleggerita
FROM python:3.10-slim

# Imposta la working directory
WORKDIR /app

# Copia il codice nell’immagine
COPY . /app

# Installa le dipendenze (FastAPI e Uvicorn)
RUN pip install fastapi "uvicorn[standard]"

# Espone la porta 8080 (porta predefinita di Code Engine)
EXPOSE 8080

# Comando di avvio: esegue Uvicorn sul file main.py (modulo 'main'), app FastAPI 'app', host e porta
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]