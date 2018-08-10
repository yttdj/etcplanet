import etcplanet.controllers
import django.conf.urls

urlpatterns = [django.conf.urls.url("^$",        etcplanet.controllers.home),
               django.conf.urls.url("^search/$", etcplanet.controllers.search)]
