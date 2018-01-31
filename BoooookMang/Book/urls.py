from django.conf.urls import url
from Book.views import *

urlpatterns = [
    # url(r'^test', test),
    # url(r'^test/(\d+){1,2}', test),
    url(r'^property/',property),
    url(r'^get/$',get),
    url(r'^get1',get1),
    url(r'^get2',get2),
    url(r'^ajax/$',ajax),
    url(r'^jsondata/$',jsondata)
]

