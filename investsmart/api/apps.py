from django.apps import AppConfig
from reco.stock_recommender import getPopularAssets

ASSET_LS = None

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        ASSET_LS = getPopularAssets()
        #print('Starting AppStarting AppStarting AppStarting App')

"""class MyAppConfig(AppConfig):
    name = 'api'
    verbose_name = "My Application"

    def ready(self):
        print('Starting App')
"""