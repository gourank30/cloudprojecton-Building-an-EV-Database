from google.appengine.ext import ndb


class data(ndb.Model):
    name = ndb.StringProperty()
    manufacturer=ndb.StringProperty()
    year=ndb.IntegerProperty()
    batterysize=ndb.IntegerProperty()
    wltprange=ndb.IntegerProperty()
    cost=ndb.IntegerProperty()
    power=ndb.IntegerProperty()
    
