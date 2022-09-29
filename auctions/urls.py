from django.urls import path

from . import views
#from cs50web_commerce import auctions

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("<int:list>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add", views.add, name="add"),
    path("delete", views.delete, name="delete")
]
