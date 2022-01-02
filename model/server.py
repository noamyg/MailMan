class Server:

    def __init__(self, name, host, port, auth, startTls, username, password):
        self.name = name
        self.host = host
        self.port = port
        self.auth = auth
        self.startTls = startTls
        self.username = username
        self.password = password

