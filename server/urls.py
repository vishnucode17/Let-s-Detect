from django.urls import path
from . import views
urlpatterns =[
    path('',views.detect,name='detect'),
    path('test',views.test_api,name='api'),
    path('decode',views.image_decode,name='image_decode'),
    path('testing',views.testing,name='testing'),
]