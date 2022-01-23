import socket

from GDServer import convertors


class Server:

    host = "www.boomlings.com"
    secret = "Wmfd2893gb7"
    port = 80
    gameVersion = 21
    binaryVersion = 35

    __accountID = None
    __gjp = None

    def __init__(self, data, id_gjp=False):

        if type(data) == tuple:  # for __enter__

            if id_gjp:
                self.set_userdata(data)
            else:
                self.set_userdata(self.convert_userdata(data))

        else:  # for req
            post = data
            self.header = _Header(post, self.host)

    @classmethod
    def set_userdata(cls, userdata):
        cls.__accountID = userdata[0]
        cls.__gjp = userdata[1]

    @classmethod
    def get_userdata(cls):
        if cls.__accountID is None and cls.__gjp is None:
            raise AttributeError("Атрибуты имени и пороля пользователя не заданы")
        return cls.__accountID, cls.__gjp

    def request(self, data):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))

            req = self.header + data

            sock.sendall(req)

            r = b""
            while b"\r\n0\r\n\r\n" not in r:
                r += sock.recv(1024)

            head, data, _ = r.decode().split("\r\n\r\n")
            if head.split("\r\n")[0] != "HTTP/1.1 200 OK":
                return -1
            data = data.split("\r\n")

            text = ""
            for i in range(1, len(data), 2):
                text += data[i]

            text = text[: text.rfind("#")]

            return text

    @classmethod
    def convert_userdata(cls, userdata):
        req = Server("/database/getGJUsers20.php")
        text = req.request(
            {
                "gameVersion": cls.gameVersion,
                "binaryVersion": cls.binaryVersion,
                "gdw": 0,
                "str": userdata[0].lower(),
                "total": 0,
                "page": 0,
                "secret": cls.secret
            }
        )
        lst = text.split(":")
        info = {}

        for i in range(len(lst) // 2):
            info[lst[i * 2]] = lst[i * 2 + 1]

        gjp = convertors.encodepassword(userdata[1])
        account_id = info["16"]

        return account_id, gjp

    def __enter__(self):
        name, psw = self.get_userdata()
        if name is None and psw is None:
            raise AttributeError("Атрибуты имени и пороля пользователя не заданы")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.set_userdata((None, None))


class _Header:

    _VOID_HEADER = (
            'POST {} HTTP/1.1\r\n' +
            'Host: {}\r\n' +
            'Accept: */*\r\n' +
            'Content-Length: {}\r\n' +
            'Content-Type: application/x-www-form-urlencoded\r\n'
            '\r\n'
    )

    def __init__(self, post, host):
        self._post = post
        self._host = host

    def __add__(self, other: dict or str) -> bytes:

        if type(other) == dict:
            data = "&".join(list(map(lambda x: x[0] + "=" + str(x[1]), list(other.items()))))
        elif type(other) == str:
            data = other
        else:
            raise TypeError("Заголовок должен суммироваться со словарём или готовой строкой тела запроса")

        s = self._VOID_HEADER.format(self._post, self._host, len(data)) + data

        return s.encode()


if __name__ == '__main__':
    a = Server("/database/getGJAccountComments20.php")
