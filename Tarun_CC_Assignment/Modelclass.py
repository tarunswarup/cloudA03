from google.appengine.ext import ndb
class TwiiterDB(ndb.Model):
    tweet = ndb.StringProperty(repeated=True)
    username = ndb.StringProperty()
    collegework = ndb.StringProperty()
    Firstname = ndb.StringProperty()
    Lastname = ndb.StringProperty()
    Email = ndb.StringProperty()
    following = ndb.StringProperty(repeated=True)
    followers = ndb.StringProperty(repeated=True)

