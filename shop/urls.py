from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("home/", views.home, name="Home"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("producthome/<str:product_name>", views.producthomeView, name="ProductHomeView"),
    path("checkouthome/<str:product_name>", views.checkouthome, name="CheckoutHome"),
    path("checkout/<int:myid>", views.checkout, name="Checkout"),
    path('signup/', views.handeSignUp, name="handleSignUp"),
    path('login/', views.handleLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout"),
    path("my_cart/", views.my_cart, name="my_cart"),
    path("delete/<int:myid>", views.delete, name="delete"),
]
