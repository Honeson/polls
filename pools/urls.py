from django.urls import path
from . import views


urlpatterns = [
     path('', views.PoolsIndexView.as_view(), name='pools_index'),
     path('<int:pk>/', views.PoolsDetailView.as_view(), name='pools_detail'),
     path('<int:pk>/results/', views.PoolsResultsView.as_view(), name='pools_results'),
     path('<int:question_id>/vote/', views.pools_vote, name='pools_vote')
     ]

