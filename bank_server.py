import json
import socket
#from threading import Thread


class BankServer():

    def __init__(self, connection, addr):
        self.connection = connection
        self.addr = addr
        self.accounts_file = "accounts/accounts.json"

    def recv_and_convert_to_json(self) -> dict:
        received_data = self.connection.recv(1024).decode()
        print(f"Data received from {self.addr}")
        converted_data = json.loads(received_data)
        return converted_data

    def ptp(self, payload):
        stringify = json.dumps(payload)
        encoded = stringify.encode()
        return encoded

    def orchestrator(self):
        received_data: dict = self.recv_and_convert_to_json()
        print(f"Received data: {received_data}")

        if received_data["action"] == 1337:
            print(received_data["data"])
            response = self.ptp(
                {"action": 1337, "data": {"msg": "message received"}})
            self.connection.sendall(response)

        elif received_data["action"] == 1:
            print(received_data["data"])
            self.write_to_json(
                new_data=received_data["data"], filename=self.accounts_file)
            response = self.ptp(
                {"action": 1, "msg": "New account added"})
            self.connection.sendall(response)

        elif received_data["action"] == 2:
            print(received_data["action"])
            all_accounts = self.view_accounts_list()
            response = self.ptp({"action": 2, "data": all_accounts})
            self.connection.sendall(response)

        elif received_data["action"] == 3:
            print(received_data["data"])
            spec_acc_info = self.view_specific_account(
                item=received_data["data"])
            response = self.ptp({"action": 3, "data": spec_acc_info})
            self.connection.sendall(response)

    def view_accounts_list(self):
        with open(self.accounts_file) as accounts:
            data = json.load(accounts)
        return data

    def write_to_json(self, new_data, filename):
        with open(filename, "r+") as accounts_open:
            data = json.load(accounts_open)
            data["accounts"].append(new_data)
            accounts_open.seek(0)
            json.dump(data, accounts_open, indent=4)

    def view_specific_account(self, item):
        with open(self.accounts_file, "r") as f:
            data = json.load(f)
            accounts = data["accounts"][item]
        return accounts


def main():
    HOST = "127.0.0.2"
    PORT = 50009

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print("Server is running...")
        try:
            while True:
                conn, addr = s.accept()
                print(f"Connection from: {addr}")
                bank1 = BankServer(conn, addr)
                bank1.orchestrator()
        except KeyboardInterrupt:
            s.close()
            exit(1)
        except Exception as e:
            s.close()
            print("Unexpected exception")
            print(e)
            exit(1)


if __name__ == "__main__":
    main()
