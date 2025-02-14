import os
from django.apps import AppConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sns.settings')


class FollowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.features.follow'
