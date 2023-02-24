class User(object):
    def __init__(self, uid, email, pwd, name, firstName, age) -> None:
        self.uid = uid
        self.email = email
        self.pwd = pwd
        self.name = name
        self.firstName = firstName
        self.age = age
    def toDict(self):
        return self.__dict__

class Posts(object):
    def __init__(self,title,body,uid):
        self.uid=uid
        self.body=body
        self.title=title
    def toDict(self):
        return self.__dict__