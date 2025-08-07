from django.urls import path
from .views import (VoteCreateView, VoteResultsView)

urlpatterns = [
    path('vote/', VoteCreateView.as_view(), name='vote_create'),
    path('results/', VoteResultsView.as_view(), name='voting_results'),
]
