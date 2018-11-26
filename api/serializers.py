from rest_framework import serializers, validators
from .models import Candidate, Election, Notification, Vote, Score


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'annotation', 'name', 'surname', 'is_student', 'scores')
        read_only_fields = ('id', 'scores')
        depth = 1


class ElectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ('id', 'date_start', 'date_end', 'is_student', 'name', 'vote_counts')
        read_only_field = ('id', 'vote_counts')


class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'election', 'sent', 'code', 'used')
        read_only_field = ('id',)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'notification', 'id_student')
        read_only_field = ('id',)


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id', 'candidate', 'election', 'votes')
        read_only_fields = ('id',)
