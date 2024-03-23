import streamlit as st 
import json
from time import sleep
from confluent_kafka import Consumer
from PIL import Image

st.set_page_config(
    page_title="Real-Time Data Dashboard",
    layout="wide",
)

if "price" not in st.session_state:
    st.session_state["price"] = []

bootstrap_servers = 'localhost:9095'
topic = 'object_detection'

conf = {'bootstrap.servers': bootstrap_servers, 'group.id': 'my_consumers'}

consumer = Consumer(conf)
consumer.subscribe([topic])

st.title("Detected objects")


im_1 = st.empty()
im_2 = st.empty()

def consume_data():
    iterations = 0
    while True:
        msg = consumer.poll(2000)

        if msg is not None:
            data = None
            try:
                data = json.loads(msg.value().decode('utf-8'))
            except json.decoder.JSONDecodeError:
                sleep(1)
                continue
            print(data)
            orig_image = Image.open(data['image_orig'])
            processed_image = Image.open(data['image_processed'])
            # if iterations % 10 == 0:
            im_1.image(orig_image, caption = 'Original image', width=480)
            im_2.image(processed_image, caption= 'Image with detected objects', width=480)
        else:
            print('Got empty message')
        iterations += 1


if __name__ == "__main__":
    consume_data()