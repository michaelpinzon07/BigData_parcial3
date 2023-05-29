
from datetime import datetime, timedelta
import random
import json
import boto3

STREAM_NAME = "kinesis"


def get_data():
    start_date = datetime(2023, 5, 25, 13, 0, 0)
    end_date = datetime(2023, 5, 25, 18, 0, 0)

    # Calcula la diferencia en días entre las fechas de inicio y fin
    delta = end_date - start_date

    random_seconds = random.randint(0, delta.total_seconds())

    random_date = start_date + timedelta(seconds=random_seconds)
    close_value = round(random.uniform(4400.000000, 4850.000000), 6)
    formatted_date = random_date.strftime('%Y-%m-%d %H:%M:%S')
    return {
        'date': formatted_date,
        'close': close_value}


def generate(stream_name, kinesis_client):
    while True:
        data = get_data()
        print(data)
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey="partitionkey")


if __name__ == '__main__':
    generate(STREAM_NAME, boto3.client('kinesis', region_name='us-east-1'))
