from rest_framework import generics, permissions, views, response, exceptions, status, pagination, viewsets

from .serializers import CandidateWriteSerializer, CandidateReadSerializer, ElectionWriteSerializer, \
    ElectionReadSerializer, NotificationWriteSerializer, NotificationReadSerializer, VoteSerializer, \
    ScoreSerializer, ElectionGetAllSerializer, AdminElectionReadSerializer, AdminElectionWriteSerializer, \
    ElectionGetResultsSerializer, NotificationInfoSerializer, AdminCandidateWriteSerializer, \
    AdminCandidateReadSerializer

from .models import Candidate, Election, Notification, Vote, Score

from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.schemas import ManualSchema

import coreapi
import coreschema

from django.conf import settings
from pytz import timezone
from datetime import datetime


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
    """
    Build a list of elections in the format:\n
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
    serializer_class = ElectionGetAllSerializer


class AdminCandidateList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Candidate.objects.all()
    get_serializer_class = get_serializer_getter(AdminCandidateWriteSerializer, AdminCandidateReadSerializer)


class AdminCandidateDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Candidate.objects.all()
    get_serializer_class = get_serializer_getter(AdminCandidateWriteSerializer, AdminCandidateReadSerializer)


class AdminElectionList(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)

    queryset = Election.objects.all()
    get_serializer_class = get_serializer_getter(AdminElectionWriteSerializer, AdminElectionReadSerializer)


class AdminElectionDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Build details about an election for admin in the format:\n
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

    permission_classes = (IsAdminUser,)

    queryset = Election.objects.all()
    get_serializer_class = get_serializer_getter(AdminElectionWriteSerializer, AdminElectionReadSerializer)
    #serializer_class = AdminElectionSerializer


class ElectionGetResults(generics.RetrieveAPIView):
    """
    Returns information about one election identified by it's ID in this format:\n
        {
            "id": ID of the election,
            "date_start": When has the election started,
            "date_end": When will the election end,
            "is_student": If is the election student,
            "name": The name of the election,
            "description": The description of the election,
            "candidates": [ Array of candidates with their info
                {
                    "id": ID of the candidate,
                    "name": Name of the candidate,
                    "surname": Surname of the candidate,
                    "is_student": If is candidate student,
                    "annotation": Description of the candidate
                    "votes": How many votes has the candidate
                }
            ]
        }
    """

    queryset = Election.objects.all()
    serializer_class = ElectionGetResultsSerializer


class NotificationInfo(generics.RetrieveAPIView):
    """
        Returns how many votes does a notification have and general info about candidates in the relevant election\n
            {
                "election_id": Id of the relevant election
                "votes_available": Number of votes available for the notification
                "candidates": [ Array of candidates with their info
                    {
                        "id": ID of the candidate,
                        "name": Name of the candidate,
                        "surname": Surname of the candidate,
                        "is_student": If is candidate student,
                        "annotation": Description of the candidate
                    }
                ]
            }
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationInfoSerializer
    lookup_field = "code"


class NotificationVote(viewsets.ViewSet):

    description = """
    Endpoint for voting. Returns how many votes were used and how many were available.\n
    {
        "votes_available": Number of votes that were available
        "votes_used": Number of votes used
    }
    """
    schema = ManualSchema(encoding="application/json", description=description, fields=[
        coreapi.Field(
            "code",
            required=True,
            location="path",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "candidates",
            required=True,
            location="body",
            schema=coreschema.Array()
        )
    ])

    @staticmethod
    def create(request, code):

        # Get candidate ids from the request
        if not request.data or request.data is None:
            return response.Response({
                "error": "Candidates field required."
            }, status=status.HTTP_400_BAD_REQUEST)
        candidate_ids = request.data

        # Fetch notification object from database
        notifications = Notification.objects.filter(code=code)
        if not notifications:
            return response.Response({
                "error": "Code is invalid."
            }, status=status.HTTP_404_NOT_FOUND)
        elif len(notifications) > 1:
            raise Exception("Multiple notifications with the same UUID exist in the database")
        notification = notifications[0]

        # Fetch candidate objects from database
        try:
            candidates = [Candidate.objects.filter(id=x)[0] for x in candidate_ids]
        except ValueError:
            return response.Response({
                "error": "At least one of the candidate ids is invalid."
            }, status=status.HTTP_404_NOT_FOUND)

        # Assert election is in progress
        if not notification.election.date_start < datetime.now(timezone(settings.TIME_ZONE)) < notification.election.date_end:
            return response.Response({
                "error": "The election isn't in progress."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Assert notification isn't already used
        if notification.used:
            return response.Response({
                "error": "This link has already been used"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Assert user hasn't sent too many votes
        votes_available = len(Vote.objects.filter(notification=notification))
        votes_used = len(candidates)
        if votes_used > votes_available:
            return response.Response({
                "error": "Too many votes were sent. This link only has %d." % votes_available
            }, status=status.HTTP_400_BAD_REQUEST)

        # Set notification as used
        notification.used = True
        notification.save()

        # Update candidate scores
        for candidate in candidates:
            try:
                score = Score.objects.filter(election=notification.election, candidate=candidate)[0]
            except IndexError:
                return response.Response({
                    "One of the selected candidates (id = %d) isn\"t in the relevant election" % candidate.id
                }, status=status.HTTP_400_BAD_REQUEST)
            score.votes += 1
            score.save()

        return response.Response({
            "votes_available": votes_available,
            "votes_used": votes_used
        }, status=status.HTTP_202_ACCEPTED)
