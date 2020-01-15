from django.conf.urls import *

from .views import *

urlpatterns = [
    url(r'^request/new/', new_request, name="new-request"),
]