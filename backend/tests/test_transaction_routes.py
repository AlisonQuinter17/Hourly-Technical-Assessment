import json
import io

def test_upload_transactions_success(client, init_database):
    csv_data = "id,date,type,amount\n1,2024-01-01,debit,100.00\n2,2024-01-02,credit,50.00"
    data = {
        'file': (io.BytesIO(csv_data.encode()), 'test.csv')
    }
    response = client.post('/transactions/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['status'] == 'pending'
    assert 'id' in json_data

def test_upload_transactions_no_file(client):
    response = client.post('/transactions/upload')
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert 'error' in json_data

def test_get_all_transactions(client, init_database):
    response = client.get('/transactions')
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert isinstance(json_data, list)
