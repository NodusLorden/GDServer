from GDServer.basereq import Server
from  GDServer.convertors import decodecomment


class GetProfileCommentsById(Server):

    def __init__(self, profile_id):
        super().__init__("/database/getGJAccountComments20.php")

        data = {
            "gameVersion": 21,
            "binaryVersion": 35,
            "gdw": 0,
            "accountID": profile_id,
            "secret": self.secret
        }

        self.response = self.request(data)

    def convert(self):

        comms = self.response.split("|")

        info = []

        for comm in comms:
            d = {}
            lst = comm.split("~")
            for i in range(len(lst) // 2):
                k = lst[i * 2]
                v = lst[i * 2 + 1]

                if k == "2":
                    d["text"] = decodecomment(v)
                elif k == "4":
                    d["likes"] = v
                elif k == "9":
                    d["date"] = v
                elif k == "6":
                    d["commentID"] = v
            info.append(d)

        return info


class GetProfileById(Server):

    def __init__(self, targetaccountid):
        super().__init__("/database/getGJAccountComments20.php")

        accountid, gjp = self.get_userdata()

        data = {
            "gameVersion": self.gameVersion,
            "binaryVersion": self.binaryVersion,
            "gdw": 0,
            "accountID": accountid,
            "gjp": gjp,
            "targetAccountID": targetaccountid,
            "secret": self.secret,
        }

        self.response = self.request(data)

    def convert(self):
        """"Тут пока пусто"""
        return None


class GetUserInfoByName(Server):

    def __init__(self, name):
        super().__init__("/database/getGJUsers20.php")

        data = {
                "gameVersion": self.gameVersion,
                "binaryVersion": self.binaryVersion,
                "gdw": 0,
                "str": name.lower(),
                "total": 0,
                "page": 0,
                "secret": self.secret
            }

        self.response = self.request(data)

    def convert(self):

        lst = self.response.split(":")
        self.info = {}

        for i in range(len(lst) // 2):
            k = lst[i * 2]
            v = lst[i * 2 + 1]
            if k == "1":
                self.info["player"] = v
            elif k == "2":
                self.info["playerID"] = v
            elif k == "13":
                self.info["coins"] = v
            elif k == "17":
                self.info["userCoins"] = v

            elif k == "6":
                continue
                # self.info["?"] = lst[i * 2 + 1]

            elif k == "9":
                self.info["icon_number"] = v
            elif k == "10":
                self.info["color1"] = v
            elif k == "11":
                self.info["color2"] = v

            elif k == "14":
                icons = {"0": "cube", "1": "ship", "2": "ball", "3": "ufo", "4": "wave", "5": "robot", "6": "spider"}
                self.info["icon_type"] = icons[v]

            elif k == "15":
                self.info["glow"] = True if v == 2 else False
            elif k == "16":
                self.info["accountID"] = v
            elif k == "3":
                self.info["stars"] = v
            elif k == "8":
                self.info["cp"] = v
            elif k == "4":
                self.info["demons"] = v

        return self.info
