import os

IS_PRODUCTION = os.environ.get('IS_PRODUCTION')
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
if IS_PRODUCTION:
    from .conf.production.settings import *
else:
    from .conf.development.settings import *
