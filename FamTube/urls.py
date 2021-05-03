from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    
    # Pages
    path('dashboard',views.DashboardPage),
    path('', lambda request: redirect('/dashboard', permanent=True)),

    # API's
    path('api/videos',views.GetAllVideos),
	path('api/search',views.Search),    
]
