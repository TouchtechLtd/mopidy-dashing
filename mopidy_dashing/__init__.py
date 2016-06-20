from __future__ import unicode_literals

import os

from mopidy import config, ext

__version__ = '0.2'

class Extension(ext.Extension):

	dist_name = 'Mopidy-Dashing'
	ext_name = 'dashing'
	version = __version__

	def get_default_config(self):
		conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf');
		return config.read(conf_file)

	def get_config_schema(self):
		schema = super(Extension, self).get_config_schema()
		schema['hostname'] = config.String()
		schema['port'] = config.Integer(optional=True)
		schema['widget'] = config.String()
		schema['auth_token'] = config.Secret()
		return schema

	def setup(self, registry):
		from .frontend import DashingFrontend
		registry.add('frontend', DashingFrontend)	
