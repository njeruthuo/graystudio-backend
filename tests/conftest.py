import os
import pytest
import django
from record.models import Client , Record,Redemption

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graystudio.settings")
django.setup()


@pytest.fixture
def create_client_fixture(db):
    return Client.objects.create(name="John Doe", number="+1234567890")


@pytest.fixture
def create_record_fixture(db, create_client_fixture):
    client = Client.objects.first()
    return Record.objects.create(client=client, amount_paid=100)


@pytest.fixture
def create_redemption_fixture(db, create_client_fixture):
    client = Client.objects.first()
    return Redemption.objects.create(client=client, points_used=10)
