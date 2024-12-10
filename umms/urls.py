from django.urls import path
from django.conf import settings
from umms import views
from django.conf.urls.static import static
# urls.py
from . import views

urlpatterns=[




  path('menu/', views.menu, name='menu'),
  path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
  path('view_cart/', views.view_cart, name='view_cart'),
  path('checkout/', views.checkout, name='checkout'),
  path('payment-success/', views.payment_success, name='payment_success'),


  path('',views.index,name='index'),
  path('signup/',views.signup,name='signup'),
  path('signin/',views.signin,name='signin'),
  path('menus/',views.menus,name='menus'),
  path('orders/',views.orders,name='orders'),
  path('contact/',views.contact,name='contact'),
  path('about/',views.about,name='about'),
  path('faq/',views.faq,name='faq'),
  path('add_food/', views.add_food, name='add_food'),
  path('edit_food/<int:food_id>/', views.edit_food, name='edit_food'),
  path('delete_food/<int:food_id>/', views.delete_food, name='delete_food')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)