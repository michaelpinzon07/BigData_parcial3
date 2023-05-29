from consumidorInferior import bollingerInf, process_records
from unittest.mock import patch


def test_bollingerInf():
    with patch('statistics.stdev') as mock_stdev:
        mock_stdev.return_value = 10.0
        precio = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
                  120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220]
        expected_result = 105.0
        actual_result = bollingerInf(precio)
        assert actual_result == expected_result


def test_process_records():
    byte_data = [{'SequenceNumber':
                  '49640710656248603271190820439928887844645997867566104626',
                  'Data': b'{"date": "2023-05-07", "close": 4721.892604}',
                  'PartitionKey': 'partitionkey'}]
    expected_result = 4721.892604
    actual_result = process_records(byte_data)
    assert actual_result == expected_result
