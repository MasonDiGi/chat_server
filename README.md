# Chat Server
A chat server made with python and socket

## Setup
- Install [python](https://www.python.org/downloads/)
- Install [node.js](https://nodejs.org/en/)
- Install all required python packages by running `python -m pip install -r requirements.txt` while in the main directory
- Install all required node.js pacakges by running `npm i` while in the `frontend` directory

## Run the software
### Server
- In the `server` directory, edit `vars.py` to have the desired IP address and port
- Run `python server.py` while in the same directory as the file

### Command-line client
- Run the server
- Enter the `client` directory
- Edit the constants at the top of the file to match the ones in `vars.py` in the `server` directory
- Run `python client.py` and enter a username
- To leave, type the chosen dc message

### API
- Run the server
- Edit `vars.py` to match the one in `server.py`
- Set flask environment variables:
    - Windows: `set FLASK_ENV=development` and `set FLASK_APP=main.py`
    - Linux: `export FLASK_ENV=development` and `export FLASK_APP=main.py`
- Execute `flask run`
- Alternatively, use software such as [gunicorn](https://gunicorn.org/) to run the server

### Website
- Run the server
- Run the API
- Go into frontend directory
- Development
    - Run `npm run start`
    - Navigate to `http://YOUR_CHOSEN_IP:3000/` in the web browser of your choice
- Production
    - Run `npm run build`
    - Use some server software (such as [nginx](https://www.nginx.com/)) and point the root to the newly created `build`
      folder
    - Navige to `http://YOUR_IP/` in the web browser of your choice
