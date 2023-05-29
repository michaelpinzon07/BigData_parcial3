import boto3
import logging
from botocore.exceptions import ClientError
import statistics

precio = []


def procesador_records(records):
    global precio
    for record in records:
        data = record['Data']
        # Decodificar el dato de la secuencia como una cadena
        data_str = data.decode('utf-8')
        # Convertir la cadena en un diccionario
        data_dict = eval(data_str)
        # Obtener el precio de la acción
        precio = data_dict['close']

        precio.append(precio)  # Agregar precio al historial

        if len(precio) >= 21:

            print(precio[:-1])
            print(len(precio[:-1]))
            precio_historial_ = precio[:-1]
            bollinger_inferior = bollinger(precio_historial_)
            print("Precio", precio)
            print("Bollinger", bollinger_inferior)
            print("\n\n")

            if precio < bollinger_inferior:
                # Si el precio está por debajo de la franja inferior
                generar_alerta(precio, bollinger_inferior)

            # Limitar el historial a los últimos 20 precios
            precio = precio[-20:]

    return precio


def bollinger(precio):
    bollinger = None
    if isinstance(precio, list) and len(precio) >= 20:
        mediaMovil = sum(precio[-20:]) / len(precio[-20:])
        stdMovil = statistics.stdev(precio[-20:])
        bollinger = mediaMovil - (2 * stdMovil)

    return bollinger


def generar_alerta(precio, bollingerInferior):
    (print(f"Alerta: el precio está por debajo de la franja inferior \
    de Bollinger ({bollingerInferior})"))
    print("Precio actual:", precio)


def main():
    stream_name = 'kinesis'

    try:
        kinesis_client = boto3.client('kinesis')

        response = kinesis_client.describe_stream(StreamName=stream_name)
        shard_id = response['StreamDescription']['Shards'][3]['ShardId']

        response = kinesis_client.get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'
        )
        shard_iterator = response['ShardIterator']
        max_records = 100
        record_count = 0

        while record_count < max_records:
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=1
            )

            shard_iterator = response['NextShardIterator']
            records = response['Records']
            record_count += len(records)
            procesador_records(records)
            try:
                print(records[0]["Data"])
            except IndexError:
                pass

    except ClientError:
        logger = logging.getLogger()
        logger.exception("Couldn't get records from stream %s.", stream_name)
        raise


if __name__ == "__main__":
    main()
