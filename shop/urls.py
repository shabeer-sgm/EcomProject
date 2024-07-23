from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('register', views.register , name='register'),
    path('login', views.login_page , name='login'),
    path('logout', views.logout_page , name='logout'),
    path('collections',views.collections , name='collections'),
    path('collections/<str:name>/',views.collectionsview , name='collections'),
    path('collections/<str:Cname>/<str:Pname>/',views.product_details , name='product_details'),
    path('cart',views.cart_page, name='cart'),
    path('addtocart', views.add_to_cart , name='addtocart'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('fav',views.favview_page, name='fav'),
    path('addfavpage', views.add_fav_page , name='addfavpage'),
    path('remove_fav/<str:fid>',views.remove_fav,name='remove_fav'),
]