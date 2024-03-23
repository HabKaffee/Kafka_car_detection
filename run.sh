#!/usr/bin/env bash
echo "To exit print \"exit\""
python src/producer.py &
streamlit run src/consumer.py &

while true; do
  string=""
  read string
  if [[ $string -eq "exit" ]]; then
    sudo kill -15 $(pidof python src/producer.py)
    sudo kill -15 $(pidof python src/consumer.py)
    docker compose down
    echo "Run stopped"