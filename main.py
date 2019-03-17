import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from add import Add
from view import View
from myuser import MyUser
from gpu import Gpu
from edit import Edit
from search import Search
from compare import Compare

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):

        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome Back'

        user = users.get_current_user()

        if user is None:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
            welcome = 'Welcome to the application'

            # generate map that contains everything that we need to pass  to the template
            template_values = {
                'url': url,
                'url_string': url_string,
                'user': user,
                'welcome': welcome
            }

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
            return

        else:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()

            if myuser is None:
                welcome = 'Welcome back to the application'
                myuser = MyUser(id=user.email(), email_address=user.email())
                myuser.email_address = user.email()
                myuser.put()

            gpus = Gpu.query().fetch(keys_only=True)
        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'welcome': welcome,
            'gpus': gpus
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', Add),
    ('/view', View),
    ('/edit', Edit),
    ('/search', Search),
    ('/compare', Compare),
], debug=True)