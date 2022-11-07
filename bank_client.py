import json
import socket
from threading import Thread
from pprint import pprint


class Client():

    def __init__(self, s):
        self.socket: socket = s
        self.client_accounts_file = 'accounts/client_accounts.json'
        self.client_new_acc_file = 'accounts/client_new_account.json'

    def print_choices(self):
        print("\nWelcome to the bank, what do you want to do?")
        print("1. Add an account")
        print("2. View all accounts")
        print("3. View specific account info")

    def orchestrator(self):
        self.print_choices()

        # packar ihop payload
        # payload = self.ptp({"action": 1337, "data": {"test": 1234}})
        action = int(input("Enter action: "))

        final_action = self.handle_send_choice(choice=action)

        #payload = self.ptp({"action": final_action})
        self.socket.sendall(final_action)  # skickar payload

        response = self.recv_and_convert_to_json()
        # väntar på svar och avkodar
        final_response = self.handle_response(server_data=response)
        print(final_response)

        print("PROGRAM IS FINISHED")

    def recv_and_convert_to_json(self):
        received_data = self.socket.recv(1024).decode()
        converted_data = json.loads(received_data)
        return converted_data

    def ptp(self, payload):
        # pack the payload
        stringify = json.dumps(payload)
        encoded = stringify.encode()
        return encoded

    def handle_response(self, server_data):
        if server_data["action"] == 1:
            response = print(server_data["msg"])
        elif server_data["action"] == 2:
            response = self.convert_customer_data(
                recvd_data=server_data["data"])
        elif server_data["action"] == 3:
            response = self.convert_spec_acc_info(
                recvd_data=server_data["data"])

        final_response = response
        return final_response

    def handle_send_choice(self, choice):
        if choice == 1:
            new_acc = self.new_account_dump()
            payload = self.ptp({"action": 1, "data": new_acc})
            return payload
        elif choice == 2:
            payload = self.ptp({"action": choice})
            self.socket.sendall(payload)
        elif choice == 3:
            spec_choice = self.view_specific_account()
            payload = self.ptp({"action": 3, "data": spec_choice})
            self.socket.sendall(payload)

        final_payload = payload
        return final_payload

    def new_account_dump(self):
        new_name = input("Enter customers name: ")
        new_balance = int(input("Enter account balance: "))
        new_client_dict = {"name": new_name, "balance": new_balance}
        return new_client_dict

    def convert_customer_data(self, recvd_data):
        i = 1
        print("\n### LIST OF ACCOUNTS ###")
        for info in recvd_data["accounts"]:
            print(f"Account #{i}")
            print(f"Name:", info["name"])
            i = i+1
            print("")
        return

    def view_specific_account(self):
        choice = int(input("What account do you want to inspect? "))
        return choice

    def convert_spec_acc_info(self, recvd_data):
        # for info in recvd_data:
        #     print(f"Customer name:", info["name"])
        #     print(f"Account balance:", info["balance"])
        #     print(" ")

        pprint(recvd_data)  # This works, but this is lazy.


def main():
    HOST = "127.0.0.2"
    PORT = 50009

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # while True:
        client = Client(s)
        client.orchestrator()

    # client.orchestrator()
    # Thread(target=client.orchestrator, args=()).start()


if __name__ == "__main__":
    main()

    # def dump_to_json(self):
    #     new_data = self.recv_and_convert_to_json()
    #     with open(self.client_accounts_file, "r+") as clients:
    #         data = json.load(clients)
    #         data = []
    #         data.append(new_data)
    #         clients.seek(0)
    #         new_info = json.dump(data, clients, indent=4)
    #     return new_info
    # def cases(self, argument):
    #     case_choice = argument
    #     match case_choice:
    #         case "all accounts":
    #             return self.convert_customer_data()
    #         case "specific account":
    #             pass

    # def handle_response(self, argument):
    #     if argument["action"] == 1:
    #         self.convert_customer_data()
    #     elif argument["data"] == "nothing":
    #         pass
    #     return


# def main():
#     HOST = "127.0.0.2"
#     PORT = 50009

#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((HOST, PORT))
#             # while True:
#             client = Client(s)
#             client.orchestrator()

#         # client.orchestrator()
#         # Thread(target=client.orchestrator, args=()).start()
#     except:
#         s.close()
#         print("something fuckedup")

    # def acc_dump_to_json(self, new_data):
    #     with open(self.client_new_acc_file, 'r+') as accounts_open:
    #         data = json.load(accounts_open)
    #         data = []
    #         data.append(new_data)
    #         accounts_open.seek(0)
    #         json.dump(data, accounts_open, indent=4)

    # def return_json(self):
    #     with open(self.client_new_acc_file, "r") as f:
    #         data = json.load(f)
    #     return data
    #     # converted_json = self.ptp(data)
    #     # return converted_json

    # def new_account(self):
    #     new_acc = self.new_account_dump()
    #     self.acc_dump_to_json(new_data=new_acc)
    #     self.return_json()
