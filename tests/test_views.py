import pytest
from django.test import Client
from django.urls import reverse

from record.models import Client as ClientModel, Record

client = Client()

@pytest.mark.django_db
def test_get_return_json():
    response = client.get(reverse('client_api_view'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_client():
    data = {
        "name": "Julius Njeru",
        "number": "+254768585724",
        "records": [  # Use a list for records
            {'amount_paid': 1000.00},
        ],
    }

    url = reverse('client_api_view')
    response = client.post(url, data, format='json')

    # Confirm that client is being created
    assert response.status_code == 201
    assert response.data['name'] == "Julius Njeru"

