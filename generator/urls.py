from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/signup/')),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('genpass/', views.genpass, name='genpass'),
    path('view_passwords/', views.view_passwords, name='view_passwords'),
]
