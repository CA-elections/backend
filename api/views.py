from rest_framework import generics, permissions, views, response, exceptions, status, pagination
from .serializers import CandidateSerializer, ElectionSerializers, NotificationSerializers, VoteSerializer, ScoreSerializer
from .models import Candidate, Election, Notification, Vote, Score


class CandidateList(generics.ListCreateAPIView):

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class ElectionList(generics.ListCreateAPIView):

    queryset = Election.objects.all()
    serializer_class = ElectionSerializers


class ElectionDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Election.objects.all()
    serializer_class = ElectionSerializers


class NotificationList(generics.ListCreateAPIView):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers


class NotificationDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers


class VoteList(generics.ListCreateAPIView):

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class ScoreList(generics.ListCreateAPIView):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


class ScoreDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
