from google.appengine.ext import ndb

class reve(ndb.Model):
    limit=ndb.StringProperty()
    carname=ndb.StringProperty()
    custrev = ndb.TextProperty()
    rate=ndb.StringProperty()
