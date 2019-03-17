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


class Search(webapp2.RequestHandler):
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
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser = ''
        if user:
            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()
        action = self.request.get('button')
        if action == 'Search':
            gpu_geometryShader = self.request.get('s_geometryShader', False) != False
            gpu_tesselationShader = self.request.get('s_tesselationShader', False) != False
            gpu_sparseBinding = self.request.get('s_sparseBinding', False) != False
            gpu_shaderInt16 = self.request.get('s_shaderInt16', False) != False
            gpu_textureCompressionETC2 = self.request.get('s_textureCompressionETC2', False) != False
            gpu_vertexPipelineStoresAndAtomic = self.request.get('s_v_p_s_a', False) != False
            logger = logging.getLogger('scope.name')
            logger.info(gpu_geometryShader)

            query1 = Gpu.query().fetch(keys_only=True)
            query2 = query1
            query3 = query1
            query4 = query1
            query5 = query1
            query6 = query1

            if gpu_geometryShader:
                query1 = Gpu.query(Gpu.geometryShader == True).fetch(keys_only=True)
            if gpu_tesselationShader:
                query2 = Gpu.query(Gpu.tesselationShader == True).fetch(keys_only=True)
            if gpu_sparseBinding:
                query3 = Gpu.query(Gpu.sparseBinding == True).fetch(keys_only=True)
            if gpu_shaderInt16:
                query4 = Gpu.query(Gpu.shaderInt16 == True).fetch(keys_only=True)
            if gpu_textureCompressionETC2:
                query5 = Gpu.query(Gpu.textureCompressionETC2 == True).fetch(keys_only=True)
            if gpu_vertexPipelineStoresAndAtomic:
                query6 = Gpu.query(Gpu.vertexPipelineStoresAndAtomic == True).fetch(keys_only=True)

            search_gpus = ndb.get_multi(set(query1).intersection(query2).intersection(query3).intersection(query4).intersection(query5).intersection(query6))

            if search_gpus:
                template_values = {
                    'myuser': myuser,
                    'gpus': search_gpus,
                }
                template = JINJA_ENVIRONMENT.get_template('search.html')
                self.response.write(template.render(template_values))
            else:
                template_values = {
                    'myuser': myuser,
                    'error': 'No GPUs Found!',
                }
                template = JINJA_ENVIRONMENT.get_template('search.html')
                self.response.write(template.render(template_values))
