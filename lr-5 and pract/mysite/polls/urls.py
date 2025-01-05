from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create/', views.create_question, name='create_question'), 
    path('search/', views.search, name='search'),
    path('<int:question_id>/analytics/', views.analytics_view, name='analytics_view'),
]

urlpatterns += [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]
urlpatterns += [
    path('<int:question_id>/analytics/', views.analytics_view, name='analytics_view'),
]