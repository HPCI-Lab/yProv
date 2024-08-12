# Usa l'immagine ufficiale di Python come base
FROM python:3.9-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Installa curl
RUN apt-get update && apt-get install -y curl

# Copia l'intero contenuto della directory del progetto nella directory di lavoro del container
COPY . .

# Assegna i permessi di esecuzione allo script 'tests.sh'
RUN chmod +x /app/tests/tests.sh

# Installa le dipendenze del progetto, se necessario
RUN pip install --no-cache-dir -r requirements.txt

# Comando di default: esegue lo script 'tests.sh'
CMD ["/app/tests/tests.sh"]
