from urls import *

urlpatterns += patterns(
    url(r'^media/(?P<filename>.*)/$','rocket_engine.views.file_serve'),
)
