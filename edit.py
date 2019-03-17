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
   loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
   extensions = ['jinja2.ext.autoescape'],
   autoescape = True
)


class Edit(webapp2.RequestHandler):
        def get(self):

                user = users.get_current_user()
                myuser = ''
                if user:
                        myuser_key = ndb.Key('MyUser', user.email())
                        myuser = myuser_key.get()
                if myuser is not None:
                        self.response.headers['Content-Type'] = 'text/html'
                        gpu_key = ndb.Key('Gpu', self.request.get('gid'))
                        gpu_info = gpu_key.get()

                        template_values = {
                                'gpu_details': gpu_info
                        }

                        template = JINJA_ENVIRONMENT.get_template('edit.html')
                        self.response.write(template.render(template_values))

        def post(self):
                user = users.get_current_user()
                myuser = ''
                if user:
                    myuser_key = ndb.Key('MyUser', user.email())
                    myuser = myuser_key.get()
                if myuser is not None:
                        if self.request.get('button') == 'Update':
                                self.response.headers['Content-Type'] = 'text/html'
                                gpu_key = ndb.Key('Gpu', self.request.get('gid'))
                                gpuInfo = gpu_key.get()
                                gpuInfo.name = self.request.get('edit_name')
                                gpuInfo.manufacturer = self.request.get('edit_manufacturer')
                                d = self.request.get('edit_dateIssued')
                                gpuInfo.dateIssued = datetime.strptime(d, '%Y-%m-%d')
                                gpuInfo.geometryShader = self.request.get('edit_geometryShader') == 'True'
                                logging.getLogger('scope.name').info(gpuInfo.geometryShader)
                                gpuInfo.tesselationShader = self.request.get('edit_tesselationShader') == 'True'
                                gpuInfo.shaderInt16 = self.request.get('edit_shaderInt16') == 'True'
                                gpuInfo.sparseBinding = self.request.get('edit_sparseBinding') == 'True'
                                gpuInfo.textureCompressionETC2 = self.request.get('edit_textureCompressionETC2',) == 'True'
                                gpuInfo.vertexPipelineStoresAndAtomic = self.request.get('edit_v_p_s_a') == 'True'
                                gpuInfo.put()

                                gpu_det = ndb.Key('Gpu', gpuInfo.name).get()
                                template_values = {
                                    'myuser': myuser,
                                    'gpu_det': gpu_det
                                }
                                template = JINJA_ENVIRONMENT.get_template('view.html')
                                self.response.write(template.render(template_values))

                        elif self.request.get('button') == 'Cancel':
                                self.redirect(' / ')
