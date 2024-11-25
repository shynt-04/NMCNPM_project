from django.apps import AppConfig
from django.db.models.signals import post_migrate

class NmcnpmappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nmcnpmapp'
    verbose_name = 'Quản lý chung cư'

