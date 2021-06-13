from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from . import auth


urlpatterns = [
    path('', views.user_operations, name='user_operations'),

    path('token/', auth.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    path('profile/', views.Profile.as_view()),

    path('recommendation/', views.Recommendation.as_view()),
    path('wishlist/', views.wishlist),
    path('watchlist/', views.watchlist),
    path('watchlist/<str:video_id>/', views.watchlist),

]
