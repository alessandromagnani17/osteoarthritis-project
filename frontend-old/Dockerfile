# Usa un'immagine base di Node.js
FROM node:14

# Imposta la directory di lavoro
WORKDIR /asw-project/frontend

# Copia il file package.json e package-lock.json
COPY package*.json ./

# Installa le dipendenze
RUN npm install

# Copia il resto del codice sorgente
COPY . .

# Costruisci il progetto Vue.js
RUN npm run build

# Espone la porta che l'applicazione utilizzerà
EXPOSE 8080

# Comando per avviare il server
CMD ["npm", "run", "serve"]