import pytest
import json
import io
from backend import models

def test_upload_transactions_success(client, init_database):
    """Test successful CSV upload"""
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
    """Test upload without file"""
    response = client.post('/transactions/upload')
    
    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert 'error' in json_data

def test_get_all_transactions(client, init_database):
    """Test getting all transactions"""
    response = client.get('/transactions')
    
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert isinstance(json_data, list)

def test_get_transaction_by_id(client, init_database):
    """Test getting a specific transaction"""
    # First create a transaction
    csv_data = "id,date,type,amount\n1,2024-01-01,debit,100.00"
    data = {
        'file': (io.BytesIO(csv_data.encode()), 'test.csv')
    }
    
    upload_response = client.post('/transactions/upload', data=data, content_type='multipart/form-data')
    transaction_id = json.loads(upload_response.data)['id']
    
    # Get the transaction
    response = client.get(f'/transactions/{transaction_id}')
    
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert json_data['id'] == transaction_id

def test_get_transaction_not_found(client):
    """Test getting a non-existent transaction"""
    response = client.get('/transactions/nonexistent-id')
    
    assert response.status_code == 404
    json_data = json.loads(response.data)
    assert 'error' in json_data
