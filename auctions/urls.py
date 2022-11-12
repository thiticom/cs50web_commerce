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
    path("delete", views.delete, name="delete"),
    path('post',views.post_comment, name="post"),
    path('submit', views.submit_bid, name="submit"),
    path('categories', views.categories, name="categories"),
    path('category/<int:cat>', views.category, name="category"),
    path('close',views.close, name="close")
]
