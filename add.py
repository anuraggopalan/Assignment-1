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


class Add(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser = ''
        if user:
            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()
        if myuser is not None:
            template_values = {
                'myuser': myuser
            }
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser = ''
        if user:
            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()
        action = self.request.get('button')
        if action == 'Add Gpu':
            gpu_name = self.request.get('add_name')
            gpu_manufacturer = self.request.get('add_manufacturer')
            d = self.request.get('add_dateIssued')
            gpu_dateIssued = datetime.strptime(d, '%Y-%m-%d')
            gpu_geometryShader = self.request.get('add_geometryShader', False) != False
            gpu_tesselationShader = self.request.get('add_tesselationShader', False) != False
            gpu_sparseBinding = self.request.get('add_sparseBinding', False) != False
            gpu_shaderInt16 = self.request.get('add_shaderInt16', False) != False
            gpu_textureCompressionETC2 = self.request.get('add_textureCompressionETC2', False) != False
            gpu_vertexPipelineStoresAndAtomic = self.request.get('add_v_p_s_a', False) != False

            gpu_check = ndb.Key('Gpu', gpu_name).get()
            if gpu_check:
                error = 'Already exists'
            else:
                gpu_query = Gpu(
                    id=gpu_name,
                    name=gpu_name,
                    manufacturer=gpu_manufacturer,
                    dateIssued=gpu_dateIssued,
                    geometryShader=gpu_geometryShader,
                    tesselationShader=gpu_tesselationShader,
                    shaderInt16=gpu_shaderInt16,
                    sparseBinding=gpu_sparseBinding,
                    textureCompressionETC2=gpu_textureCompressionETC2,
                    vertexPipelineStoresAndAtomic=gpu_vertexPipelineStoresAndAtomic,
                )

                gpu_query.put()
                self.redirect('/')
