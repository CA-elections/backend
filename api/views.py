from rest_framework import generics, permissions, views, response, exceptions, status, pagination
from .serializers import CandidateSerializer, ElectionSerializers, NotificationSerializers, VoteSerializer, ScoreSerializer
from .models import Candidate, Election, Notification, Vote, Score


class CandidateList(generics.ListCreateAPIView):

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

