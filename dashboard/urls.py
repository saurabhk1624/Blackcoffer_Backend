from django.urls import path,include
from .views import *
urlpatterns = [
    path('import/',import_data),
    path('statistics/',dashboard_statistics),

]
