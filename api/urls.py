from django.conf.urls import url, include
from django.views import generic
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CandidateList, CandidateDetails, ElectionList, ElectionDetails, NotificationList, NotificationDetails, VoteList, VoteDetails, ScoreList, ScoreDetails

urlpatterns = [
    url(r'^$', get_schema_view(title="API for Ca elections")),
    url(r'^docs/', include_docs_urls(title="CA elections API")),
    url(r'^auth/', include('rest_framework.urls')),
    url(r'^candidate/$', CandidateList.as_view()),
    url(r'^candidate/(?P<pk>[0-9]+)/$', CandidateDetails.as_view()),
    url(r'^election/$', ElectionList.as_view()),
    url(r'^election/(?P<pk>[0-9]+)/$', ElectionDetails.as_view()),
    url(r'^notification/$', NotificationList.as_view()),
    url(r'^notification/(?P<pk>[0-9]+)/$', NotificationDetails.as_view()),
    url(r'^vote/$', VoteList.as_view()),
    url(r'^vote/(?P<pk>[0-9]+)/$', VoteDetails.as_view()),
    url(r'^score/$', ScoreList.as_view()),
    url(r'^score/(?P<pk>[0-9]+)/$', ScoreDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
