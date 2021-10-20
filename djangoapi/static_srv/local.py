import os

from djangoapi.settings.base import BASE_DIR


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'my_static'),
]


STATIC_ROOT = os.path.join(BASE_DIR,'static_local_cdn', 'static_root') # 'djangoapp',

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static_local_cdn', 'media_root')

PROTECTED_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_local_cdn","protected")

