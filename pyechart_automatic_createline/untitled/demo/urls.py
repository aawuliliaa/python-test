
from django.urls import path,re_path

from demo import views
app_name = "demo"
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    # re_path(r'^bar/$', views.BarView.as_view(), name='bar'),
    re_path(r'^index/$', views.IndexView.as_view(), name='bar_index'),
# re_path(r'^line/$', views.LineView.as_view(), name='line'),
re_path(r'^lineUpdate/$', views.ChartUpdateView.as_view(), name='lineUpdate'),
]