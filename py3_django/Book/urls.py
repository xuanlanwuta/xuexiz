from django.conf.urls import include, url
from Book.views import index,bookhtml,renwu

urlpatterns = {
    url (r'^index/$' , index) ,
    url (r'^bookhtml/$' , bookhtml),
    url(r'^(\d)/$',renwu)
}