#!/bin/bash

# Percorso della cartella
DIR="/Users/alessandromagnani/Desktop/Università/applicazioni-e-servizi-web/asw-project"

# File di output
OUTPUT="$DIR/elenco_file.txt"

# Trova tutti i file e le directory, escludendo node_modules, venv e file nascosti
find "$DIR" \( -path "$DIR/frontend/node_modules" -o -path "$DIR/backend/venv" -o -name ".*" \) -prune -o -print | sed -e "s|$DIR/||" -e "s|[^/]*/|    |g" -e "s|__|├── |g" -e "s|$|/|" > "$OUTPUT"

