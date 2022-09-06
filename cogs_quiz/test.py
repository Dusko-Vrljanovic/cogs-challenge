from .settings import *

DATABASES = {
    'default': DATABASES['default']
}
DATABASES['default']['NAME'] = 'test_' + DATABASES['default']['NAME']
