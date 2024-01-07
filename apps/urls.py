from django.urls import path

from apps.views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("all-farm/", AllFarmView.as_view(), name="all_farm"),
    path("blog/", BlogView.as_view(), name="blog"),
    path("blog-single/", BlogSingleView.as_view(), name="blog_single"),
    path("contact/", ContactView.as_view(), name="contact"),
]
