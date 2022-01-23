from GDServer import gdrequests as gd


password = None
name = None

with gd.Server((name, password)):
    myid = gd.GetUserInfoByName(name).convert()["accountID"]
    res = gd.GetProfileCommentsById(myid).convert()

    print(res)


gjp = None
accountID = None

with gd.Server((accountID, gjp), id_gjp=True):
    myid = gd.GetUserInfoByName(name).convert()["accountID"]
    res = gd.GetProfileCommentsById(myid).convert()

    print(res)
