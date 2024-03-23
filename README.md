To setup environment run `set_up_env.sh` under bash
```shell
chmod +x set_up_env.sh
./set_up_env.sh
```
or
```shell
bash ./set_up_env.sh
```
NOTE: Dataset is donwloading from Google Drive because it is reduced dataset https://www.kaggle.com/datasets/javiersanchezsoriano/traffic-images-captured-from-uavs (35 GB reduced to 5 GB)

To run app enter following commands
```shell
source venv/bin/activate
docker compose up -d
```
And two .py files should be ran simultaneously (code shown below)
```shell
python src/producer.py &
streamlit run consumer.py
```
To stop execution run
```shell
sudo kill -15 $(pidof python src/producer.py)
```
to kill producer.py and just regular Ctrl+C to interrupt consumer.py

Enjoy usage!
