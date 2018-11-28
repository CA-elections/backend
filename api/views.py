from rest_framework import generics, permissions, views, response, exceptions, status, pagination, viewsets

from .serializers import CandidateWriteSerializer, CandidateReadSerializer, ElectionWriteSerializer, ElectionReadSerializer, NotificationWriteSerializer, NotificationReadSerializer, VoteSerializer, ScoreSerializer, ElectionGetAllSerializer, AdminElectionSerializer, ElectionGetResultsSerializer, NotificationInfoSerializer

from .models import Candidate, Election, Notification, Vote, Score


def get_serializer_getter(WriteSerializer, ReadSerializer):

    def get_serializer_class(self):
        if not self.request:
            return WriteSerializer
        method = self.request.method
        if method == 'PUT' or method == 'POST' or method == 'PATCH':
            return WriteSerializer
        else:
            return ReadSerializer

    return get_serializer_class


class CandidateList(generics.ListCreateAPIView):

    queryset = Candidate.objects.all()
    get_serializer_class = get_serializer_getter(CandidateWriteSerializer, CandidateReadSerializer)


class CandidateDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Candidate.objects.all()
    get_serializer_class = get_serializer_getter(CandidateWriteSerializer, CandidateReadSerializer)


class ElectionList(generics.ListCreateAPIView):
    """Build a list of elections in the format:
       {
         "id": id,
         "date_start": date_start,
         "date_end": date_end,
         "is_student": is_student,
         "description": description,
         "name": name
       }
    """
    queryset = Election.objects.all()
    get_serializer_class = get_serializer_getter(ElectionWriteSerializer, ElectionReadSerializer)


class ElectionDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Election.objects.all()
    get_serializer_class = get_serializer_getter(ElectionWriteSerializer, ElectionReadSerializer)


class NotificationList(generics.ListCreateAPIView):

    queryset = Notification.objects.all()
    get_serializer_class = get_serializer_getter(NotificationWriteSerializer, NotificationReadSerializer)


class NotificationDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Notification.objects.all()
    get_serializer_class = get_serializer_getter(NotificationWriteSerializer, NotificationReadSerializer)


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


class ElectionGetAll(generics.ListAPIView):

    queryset = Election.objects.all()
    serializer_class = ElectionGetAllSerializer


class AdminElectionDetails(generics.RetrieveAPIView):
    """Build details about an election for admin in the format:
       {
         "id": id,
         "date_start": date_start,
         "date_end": date_end,
         "is_student": is_student,
         "description": description,
         "name": name,
         "candidates": [{
           "id": candidate_id,
           "name": candidate_name,
           "surname": candidate_surname,
           "is_student": candidate_is_student,
           "annotation": candidate_annotation,
           "votes": candidate_votes
         }, ...]
       }
    """
    queryset = Election.objects.all()
    serializer_class = AdminElectionSerializer


class ElectionGetResults(generics.RetrieveAPIView):

    queryset = Election.objects.all()
    serializer_class = ElectionGetResultsSerializer


class NotificationInfo(generics.RetrieveAPIView):

    queryset = Notification.objects.all()
    serializer_class = NotificationInfoSerializer
    lookup_field = "code"
