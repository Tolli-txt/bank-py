# Banken

My assignment for Nackademin "Programmering i Python" course.

`bank_server.py` is the main server file.

`bank_client.py` is the main client file.

In the tests folder you will find the `test_bank.py` file which has been used for writing unittests.


### How to run
1. Open up two seperate command interpreters.
2. `py bank_server.py` to launch the server.
3. `py bank_client.py` to launc the client. NOTE: The client will not launch if the server is not turned on before.
4. Interact with the menu for the client CLI

#### How to run tests
1. Enter virtual environment.

Linux / OSX
>`python -m venv .venv  # could also be python3`
>
>`source .venv/bin/activate`

Windows - cmd.exe
>`python -m venv .venv`
>
>`.venv\Scripts\activate.bat`

Windows - PowerShell
>`py -m venv .venv`
>
>`.\.venv\Scripts\Activate.ps1`

2. Install requirements

`pip install -r requirements.txt`
3. In the command line, write `pytest tests/test_bank.py` or just `tox`
