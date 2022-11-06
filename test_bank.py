from bank_server import Customer
from bank_client import Client

client1 = Client("")
customer1 = Customer("","")

def test_pack_the_payload_client():
    assert client1.ptp({"test": 1234}) == b'{"test": 1234}'

def test_pack_the_payload_customer():
    assert customer1.ptp({"test": 1234}) == b'{"test": 1234}'

def test_understanding_client_customer_ptp():
    assert customer1.ptp({"test": 1234}) == client1.ptp({"test": 1234}) == b'{"test": 1234}'