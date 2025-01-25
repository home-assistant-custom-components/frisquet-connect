import json

class AuthenticationRequest:
    def __init__(self, email: str, password: str, locale: str="fr", type_client: str="IOS"):
        self.locale = locale
        self.email = email
        self.password = password
        self.type_client = type_client

    def to_dict(self):
        return self.__dict__
    
    def __repr__(self):
        return json.dumps(self.__dict__)

