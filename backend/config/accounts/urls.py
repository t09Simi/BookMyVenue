from django.urls import path
from .views import VenueListView, VenueSubmitView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("venues/", VenueListView.as_view(), name="venue-list"),
    path("venues/<int:pk>/submit/", VenueSubmitView.as_view(), name="venue-submit"),
]