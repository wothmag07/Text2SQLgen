#!/bin/bash
set -e

echo "Loading CSV data into PostgreSQL..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    \COPY llm.heartattack_data FROM '/data/heart_attack_prediction_dataset.csv' WITH CSV HEADER;
    \COPY llm.breastcancer_data FROM '/data/breast-cancer.csv' WITH CSV HEADER;
    \COPY llm.livercirrhosis_data FROM '/data/cirrhosis.csv' WITH CSV HEADER;
    \COPY llm.diabetes_data FROM '/data/diabetes.csv' WITH CSV HEADER;
    \COPY llm."glaucoma_Data" FROM '/data/glaucoma_dataset.csv' WITH CSV HEADER;
EOSQL

echo "All CSV data loaded successfully!"
