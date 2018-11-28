from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views

from .views import ElectionGetAll, CandidateList, CandidateDetails, ElectionList, ElectionDetails, NotificationList, NotificationDetails, VoteList, VoteDetails, ScoreList, ScoreDetails, AdminElectionDetails, ElectionGetResults

urlpatterns = [
    url(r'^$', get_schema_view(title="API for Ca elections")),
    url(r'^docs/', include_docs_urls(title="CA elections API")),
    url(r'^token-auth/', views.obtain_auth_token),

    url(r'^election/$', ElectionGetAll.as_view()),
    url(r'^election/(?P<pk>[0-9]+)/$', ElectionGetResults.as_view()),

    url(r'^test/candidate/$', CandidateList.as_view()),
    url(r'^test/candidate/(?P<pk>[0-9]+)/$', CandidateDetails.as_view()),
    url(r'^test/election/$', ElectionList.as_view()),
    url(r'^test/election/(?P<pk>[0-9]+)/$', ElectionDetails.as_view()),
    url(r'^test/notification/$', NotificationList.as_view()),
    url(r'^test/notification/(?P<pk>[0-9]+)/$', NotificationDetails.as_view()),
    url(r'^test/vote/$', VoteList.as_view()),
    url(r'^test/vote/(?P<pk>[0-9]+)/$', VoteDetails.as_view()),
    url(r'^test/score/$', ScoreList.as_view()),
    url(r'^test/score/(?P<pk>[0-9]+)/$', ScoreDetails.as_view()),
    url(r'^admin/election/(?P<pk>[0-9]+)/$', AdminElectionDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
