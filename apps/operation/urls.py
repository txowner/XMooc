
from django.conf.urls import url

from .views import UserAskView, FavView


urlpatterns = [
    url(r'^ask/$', UserAskView.as_view(), name='ask'),
    url(r'^fav/$', FavView.as_view(), name='fav'),
]
