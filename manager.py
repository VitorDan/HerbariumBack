from api import create_app

app = create_app()

from api import socket,core
    
if __name__ == '__main__':
    socket.run(app, debug=True)