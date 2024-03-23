#!/usr/bin/env bash
echo "Creating venv for project"
python3 -m venv venv
source ./venv/bin/activate
echo "Installing packages..."
pip install -r requirements.txt
mkdir data/
cd data/ && gdown 1OBhVHQ758Kdrw1fvJR_qFq3OuhJ0YHgN && tar -xvf traffic_dataset.tar.gz && rm traffic_dataset.tar.gz && cd ../
echo "Starting docker compose for Kafka"
docker compose up -d
echo "Setup done!"