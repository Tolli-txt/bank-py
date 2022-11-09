import pytest
import builtins
from _pytest.monkeypatch import MonkeyPatch
from unittest import mock
from unittest.mock import patch


from bank_server import BankServer
from bank_client import Client

server1 = BankServer("", "")
client1 = Client("")


@patch('builtins.input', side_effect=['Antanas', 1337])
def test_new_account_dump(input):
    assert client1.new_account_dump() == {"name": 'Antanas', "balance": 1337}


@mock.patch("builtins.input")
def test_new_account_dump(mock_input):
    mock_input.side_effect = ["Oskar", 50000]
    assert client1.new_account_dump() == {'balance': 50000, 'name': 'Oskar'}


def test_pack_the_payload_client():
    assert client1.ptp({"test": 1234}) == b'{"test": 1234}'


def test_pack_the_payload_server():
    assert server1.ptp({"action": 1}) == b'{"action": 1}'


def test_understanding_client_customer_ptp():
    assert server1.ptp({"test": 1234}) == client1.ptp({"test": 1234}) == b'{"test": 1234}'


@patch('builtins.input', side_effect=[1])
def test_view_specific_account(input):
    assert client1.view_specific_account() == 1


# def test_pack_the_payload_customer_2():
#     test_dict = {
#         "name": "pyTest",
#         "balance": 2000
#     }
#     assert customer1.ptp({"action": 1, "data": test_dict}) == b'{"action": 1, "data": test_dict}'


#
# @patch('client.get_input', return_value="Antanas")
# @patch('client.get_input', return_value=1337)
# def test_new_account_dump(name, balance):
#     print(name)
#     print(balance)

#assert client1.new_account_dump(lambda x: 1) == (1, 1)

# def test_new_account_dump(input, money):
#     print(input)
#     print(money)

# def test_new_account_dump(monkeypatch):
#     inputs = iter(['Testguy', 1337])
#     monkeypatch.setattr('builtins.input', lambda _: next(inputs))
#     result = client1.new_account_dump()
#     assert result == "New account created"


# def test_new_account_dump():
#     client1
#     set_keyboard_input(["venvGuy", "1337"])
#     client1.new_account_dump()
#     output = get_display_output()
#     assert output == ["Enter customers name: ", "Enter account balance: "]
