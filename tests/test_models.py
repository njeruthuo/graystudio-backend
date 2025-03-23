import pytest

from record.models import Client


@pytest.mark.django_db
def test_client_created(create_client_fixture):
    client = list(Client.objects.all())

    assert len(client) == 1



# test if record creation updates the clients points
@pytest.mark.django_db
def test_record_creation(create_client_fixture, create_record_fixture, create_redemption_fixture):
    client = Client.objects.first()

    # confirms that the record created added points to the client
    assert client.total_points == 10


# test if redemption reduces the amount of total_points
@pytest.mark.django_db
def test_redemption_reduces_total_points(create_client_fixture, create_record_fixture):
    client = Client.objects.first()

    # test that redeeming ten points will result in 0 points for the client
    client.redeem_points(10)

    assert client.total_points == 0


# test if a larger redemption attempt will throw an error
@pytest.mark.django_db
def test_redemption_throws_error_on_less_points(create_client_fixture, create_record_fixture):
    client = Client.objects.first()

    assert client.total_points == 10

    # assert that this will throw a validation error since we are redeeming more than we have
    with pytest.raises(ValueError, match="Not enough points to redeem"):
        client.redeem_points(100)
