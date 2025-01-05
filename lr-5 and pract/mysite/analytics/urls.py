from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionAnalyticsViewSet

router = DefaultRouter()
router.register('analytics', QuestionAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', QuestionAnalyticsViewSet.as_view({'get': 'list'})),
    path('analytics/<int:pk>/', QuestionAnalyticsViewSet.as_view({'get': 'retrieve'})),
]
