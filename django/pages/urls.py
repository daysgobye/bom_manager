from django.urls import path

from .views import HomePageView, libraryPageView, checkout,add

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("library/", libraryPageView, name="library"),
    path("library/checkout",checkout,name="checkout"),
    path("library/add",add,name="add")
]
