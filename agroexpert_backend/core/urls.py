# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('login/', views.login_view, name='login'),
#     path('signup/', views.signup, name='signup'),
#     path('logout/', views.logout_view, name='logout'),
#     path('crop/', views.crop_page, name='crop_page'),
# ]


# from django.contrib import admin
# from django.urls import path, include
# from core import views

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     path('', views.home, name='home'),
#     path('login/', views.login_view, name='login'),
#     path('signup/', views.signup, name='signup'),
#     # path('logout/', views.logout_view, name='logout'),
#     path('crop/', views.crop_page, name='crop_page'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
    

#     path('login/', views.login_view, name='login'),
#     path('signup/', views.signup, name='signup'),
#     path('logout/', views.logout_view, name='logout'),

#     path('dashboard/', views.dashboard, name='dashboard'),

#     path('crop/', views.crop_page, name='crop_page'),

#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('crop/', views.crop_page, name='crop'),
#     path('soil-test/', views.soil_test, name='soil_test'),
#     path('weather/', views.weather, name='weather'),
#     path('yield/', views.yield_prediction, name='yield_prediction'),
#     path('fertilizer/', views.fertilizer, name='fertilizer'),
# ]



from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('scheme/', views.scheme, name='scheme'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crop/', views.crop_page, name='crop'),

    path('soil-test/', views.soil_test, name='soil_test'),
    path('weather/', views.weather, name='weather'),
    path('fertilizer/', views.fertilizer, name='fertilizer'),
    path('yield/', views.yield_prediction, name='yield_prediction'),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-users/", views.admin_users, name="admin_users"),
    path("delete-user/<int:user_id>/", views.delete_user, name="delete_user"),
    path("admin-soil-requests/", views.admin_soil_requests, name="admin_soil_requests"),
    path("update-soil-status/<int:req_id>/<str:status>/", views.update_soil_status, name="update_soil_status"),
    path("admin-reports/", views.admin_reports, name="admin_reports"),
]