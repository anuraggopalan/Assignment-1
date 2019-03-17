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


class Compare(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser = ''
        if user:
            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()
        if myuser is not None:

            gpus = Gpu.query().fetch(keys_only=True)
            template_values = {
                'myuser': myuser,
                'available_gpus': gpus
            }
        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser = ''
        if user:
            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()
        action = self.request.get('button')
        if action == 'Compare':

            gpu1_key = self.request.get('gpu1_key')
            gpu2_key = self.request.get('gpu2_key')
            logger = logging.getLogger('scope.name')
            logger.info(gpu1_key)
            gpus = Gpu.query().fetch(keys_only=True)

            if gpu1_key == gpu2_key or gpu1_key == 'Select One' or gpu2_key == 'Select One':
                template_values = {
                    'myuser': myuser,
                    'error': 'Please select two different GPUs to Compare Successfully',
                    'available_gpus': gpus
                }

                template = JINJA_ENVIRONMENT.get_template('compare.html')
                self.response.write(template.render(template_values))
            else:
                gpu1 = ndb.Key('Gpu', gpu1_key).get()
                gpu2 = ndb.Key('Gpu', gpu2_key).get()

                template_values = {
                    'myuser': myuser,
                    'gpu1': gpu1,
                    'gpu2': gpu2,
                    'available_gpus': gpus,
                }
                template = JINJA_ENVIRONMENT.get_template('compare.html')
                self.response.write(template.render(template_values))
