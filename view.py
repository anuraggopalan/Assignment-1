import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from datetime import datetime
from gpu import Gpu
from myuser import MyUser
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class View(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser = ''
        if user:
            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()
        if myuser is not None:

            gpu_id = self.request.get('id')

            gpu_det = ndb.Key('Gpu', gpu_id).get()

            if gpu_det:
                template_values = {
                    'myuser': myuser,
                    'gpu_det': gpu_det
                }
                template = JINJA_ENVIRONMENT.get_template('view.html')
                self.response.write(template.render(template_values))
            else:
                error = 'Does not exist'