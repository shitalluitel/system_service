import mongoengine as me


class User(me.Document):
    username = me.StringField(required=True)
    password = me.StringField()
    devices = me.ListField(me.StringField())
    date_created = me.DateTimeField()

    def verify_password(self, password):
        # we can make it more secure by implementing different cryptographic
        # functions to hash and un-hash password.(Encryption /Decryption)
        return password == self.password
