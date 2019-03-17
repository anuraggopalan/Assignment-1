from google.appengine.ext import ndb
from gpu import Gpu

class MyUser(ndb.Model):
    name = ndb.StringProperty()
    email_address = ndb.StringProperty()