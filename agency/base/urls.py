from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register-agency/', views.register_agency, name='register_agency'),
    path('register-user/', views.register_user, name='register_user'),
    path('update-user/', views.update_user, name='update-user'),

    path('', views.home, name='home'),
    path('arrangement/<str:pk>', views.arrangement, name='arrangement'),

    path('create-arrangement/', views.create_arrangement, name='create-arrangement'),
    path('update-arrangement/<str:pk>', views.update_arrangement, name='update-arrangement'),
    path('delete-arrangement/<str:pk>', views.delete_arrangement, name='delete-arrangement'),
    path('reserve-arrangement/<str:pk>', views.reserve_arrangement, name='reserve-arrangement')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
