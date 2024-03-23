from confluent_kafka import Producer
import json
import os
import time
from PIL import Image
from model import YOLOv8

bootstrap_servers = 'localhost:9095'
topic = 'object_detection'

conf = {'bootstrap.servers': bootstrap_servers}
producer_1 = Producer(conf)
producer_2 = Producer(conf)

folder_to_store_processed = './data/processed_data/'
base_dir_originals = './data/dataset/'

def get_processed_image(image_id, data, processor) -> None:
    image = data[image_id]
    res = processor.predict(f'{base_dir_originals}/{image}')
    processed_image, _, _, _ = processor.plot_bboxes(res)
    processed_image_to_save = Image.fromarray(processed_image)
    processed_image_to_save.save(f'{folder_to_store_processed}/processed_{image_id}.jpg')

def make_json(data, image_id):
    image = data[image_id]
    image_data = {
        'image_id': image_id,
        'image_orig': f'{base_dir_originals}/{image}',
        'image_processed': f'{folder_to_store_processed}/processed_{image_id}.jpg'
    }
    return image_data

def produce_data():
    data_to_be_produced = sorted(os.listdir(base_dir_originals))
    print(f'Found {len(data_to_be_produced)} images in stream. Processing...')
    processor = YOLOv8()
    if not os.path.isdir(folder_to_store_processed):
        os.makedirs(folder_to_store_processed)
    image_id = 0
    while True:
        if image_id >= len(data_to_be_produced) - 2:
            image_id = 0
        get_processed_image(image_id=image_id,
                            data=data_to_be_produced,
                            processor=processor)
        get_processed_image(image_id=image_id + 1,
                            data=data_to_be_produced,
                            processor=processor)
        image_data_1 = make_json(data=data_to_be_produced,
                                image_id=image_id)
        image_data_2 = make_json(data=data_to_be_produced,
                                image_id=image_id + 1)
        image_id += 2
        time.sleep(0.1)
        producer_1.produce(topic, key='1', value=json.dumps(image_data_1))
        producer_1.flush()
        producer_2.produce(topic, key='1', value=json.dumps(image_data_2))
        producer_2.flush()
        print(f'Produced: {image_data_1}\t{image_data_2}')

if __name__ == "__main__":
    produce_data()