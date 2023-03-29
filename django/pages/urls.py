from django.urls import path

from .views import HomePageView, libraryPageView, checkout,add,find

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("library/", libraryPageView, name="library"),
    path("library/add",add,name="add"),
    path("library/checkout",checkout,name="checkout"),
    path("library/checkout/find/",find,name="find"),
]
