from django.urls import path
from . import views

urlpatterns = [
    
    # Pages
    path('dashboard',views.DashboardPage),

    # API's
    path('api/videos',views.GetAllVideos),
	path('api/search',views.Search),    
]
