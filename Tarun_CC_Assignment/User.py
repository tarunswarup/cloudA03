from google.appengine.ext import ndb
class User(ndb.Model):
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    age = ndb.StringProperty()
