import base64


def encodepassword(psw: str):
    return base64encode(xorpsw(psw, 37526))


def decodepassword(gjp: str):
    return xorpsw(base64decode(gjp), 37526)


def decodecomment(text: str):
    return base64decode(text)


def encodecomment(text: str):
    return base64encode(text)


def xorpsw(psw: str, key: int):
    key = str(key)
    xst = ""
    for i in range(len(psw)):
        xst += chr(ord(psw[i]) ^ ord(key[i % len(key)]))
    return xst


def base64decode(text: str):
    return base64.b64decode(text.replace("_", "/").replace("-", "+")).decode("ASCII")


def base64encode(text: str):
    return base64.b64encode(text.encode()).decode().replace("/", "_").replace("+", "-")
