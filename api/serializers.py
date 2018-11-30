from django.db.models import Sum, functions
from rest_framework import serializers, validators
from .models import Candidate, Election, Notification, Vote, Score
from django.conf import settings
import datetime
import pytz
import sys

tz = pytz.timezone(settings.TIME_ZONE)


class CandidateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'name', 'surname', 'is_student', 'annotation')


class CandidateReadSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'is_student': instance.is_student,
            'name': instance.name,
            'surname': instance.surname,
            'annotation': instance.annotation,
            'elections': [
                {
                    'id': election.id,
                    'date_start': election.date_start,
                    'date_end': election.date_end,
                    'is_student': election.is_student,
                    'name': election.name,
                    'votes': Score.objects.filter(election=election).aggregate(votes_sum=functions.Coalesce(Sum('votes'), 0))['votes_sum'],
                    'candidates': [
                        {
                            'id': candidate.id,
                            'votes': votes,
                        } for candidate, votes in map(lambda x: (x.candidate, x.votes), Score.objects.filter(election=election))
                    ]
                } for election in map(lambda x: x.election, Score.objects.filter(candidate=instance))
            ],
        }

    def to_internal_value(self, data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class ElectionWriteSerializer(serializers.ModelSerializer):
    candidates = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all(), many=True)

    def create(self, validated_data):
        candidates_data = validated_data.pop('candidates')
        election = Election.objects.create(**validated_data)
        for candidate in candidates_data:
            Score.objects.create(
                candidate=candidate,
                election=election,
            )
        return election

    def update(self, instance, validated_data):
        try:
            candidates_data = list(map(lambda x: x, validated_data.pop('candidates'))),
            print(candidates_data)
            sys.stderr.write(str(candidates_data) + "\n")
            for score in Score.objects.filter(election=instance):
                if score.candidate not in candidates_data:
                    score.delete()

                candidates_data = list(filter(lambda x: x != score.candidate, candidates_data))

            for candidate in candidates_data:
                Score.objects.create(
                    candidate=candidate,
                    election=instance,
                )
        except KeyError:
            pass

        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.is_student = validated_data.get('is_student', instance.is_student)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance

    class Meta:
        model = Election
        fields = ('id', 'date_start', 'date_end', 'is_student', 'name', 'candidates', 'description')


class ElectionReadSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'date_start': instance.date_start,
            'date_end': instance.date_end,
            'is_student': instance.is_student,
            'name': instance.name,
            'votes': Score.objects.filter(election=instance).aggregate(votes_sum=functions.Coalesce(Sum('votes'), 0))['votes_sum'],
            'description': instance.description,
            'candidates': [
                {
                    'id': score.candidate.id,
                    'name': score.candidate.name,
                    'surname': score.candidate.surname,
                    'is_student': score.candidate.is_student,
                    'annotation': score.candidate.annotation,
                    'votes': score.votes,
                } for score in Score.objects.filter(election=instance)],
        }

    def to_internal_value(self, data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class NotificationWriteSerializer(serializers.ModelSerializer):
    students = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def create(self, validated_data):
        students_data = validated_data.pop('students')
        notification = Notification.objects.create(**validated_data)
        for student_id in students_data:
            Vote.objects.create(
                notification=notification,
                id_student=student_id,
            )
        return notification

    def update(self, instance, validated_data):
        try:
            students_data = validated_data.pop('students')
            for vote in Vote.objects.filter(notification=instance):
                if vote.id_student not in students_data:
                    vote.delete()

                students_data = list(filter(lambda x: x != vote.id_student, students_data))

            for student_id in students_data:
                Vote.objects.create(
                    notification=instance,
                    id_student=student_id,
                )
        except KeyError:
            pass

        instance.election = validated_data.get('election', instance.election)
        instance.sent = validated_data.get('sent', instance.sent)
        instance.code = validated_data.get('code', instance.code)
        instance.used = validated_data.get('used', instance.used)
        instance.save()

        return instance

    class Meta:
        model = Notification
        fields = ('id', 'election', 'sent', 'code', 'used', 'students')


class NotificationReadSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'sent': instance.sent,
            'code': instance.code,
            'used': instance.used,
            'students': [
                {
                    'id': vote.id_student,
                } for vote in Vote.objects.filter(notification=instance)],
        }

    def to_internal_value(self, data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'notification', 'id_student')
        read_only_fields = ('id',)


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id', 'candidate', 'election', 'votes')
        read_only_fields = ('id',)


class ElectionGetAllSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'date_start': instance.date_start,
            'date_end': instance.date_end,
            'is_student': instance.is_student,
            'description': instance.description,
            'name': instance.name,
        }
        # adding information about who has won this election
        if instance.date_end < datetime.datetime.now(tz):
            totalvotes = 0
            scores = Score.objects.filter(election=instance).order_by('-votes')
            for score in scores:
                totalvotes += score.votes
            if totalvotes == 0:
                return data
            samevotes = 1
            while samevotes < scores.count():
                if scores[samevotes - 1].votes == scores[samevotes].votes:
                    samevotes += 1
                else:
                    break
            data['percentage'] = scores[0].votes / totalvotes
            data['num_winners'] = samevotes
            if samevotes == 1:
                data['winner_name'] = scores[0].candidate.name
                data['winner_surname'] = scores[0].candidate.surname
        return data

    def to_internal_value(self, data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class AdminElectionReadSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        possible_votes = 0
        for notif in Notification.objects.filter(election=instance):
            possible_votes += Vote.objects.filter(notification=notif).count()
        votes_cast = 0
        for score in Score.objects.filter(election=instance):
            votes_cast += score.votes
        return {
                'id': instance.id,
                'date_start': instance.date_start,
                'date_end': instance.date_end,
                'is_student': instance.is_student,
                'name': instance.name,
                'description': instance.description,
                'candidates': [
                {
                    'id': score.candidate.id,
                    'name': score.candidate.name,
                    'surname': score.candidate.surname,
                    'is_student': score.candidate.is_student,
                    'annotation': score.candidate.annotation,
                    'votes': score.votes,
                } for score in Score.objects.filter(election=instance).order_by('-votes')],
                'possible_votes': possible_votes,
                'votes_cast': votes_cast,
        }

    def to_internal_value(self, data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class AdminElectionWriteSerializer(serializers.ModelSerializer):
    candidates = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all(), many=True)

    def create(self, validated_data):
        candidates_data = validated_data.pop('candidates')
        election = Election.objects.create(**validated_data)
        for candidate in candidates_data:
            Score.objects.create(
                candidate=candidate,
                election=election,
            )
        return election

    def update(self, instance, validated_data):
        candidates_data = validated_data.pop('candidates')
        for score in Score.objects.filter(election=instance):
            if score.candidate.id not in candidates_data:
                score.candidate.delete()

            candidates_data = list(filter(lambda x: x != score.candidate.id, candidates_data))

        for candidate in candidates_data:
            Score.objects.create(
                candidate=candidate,
                election=instance,
            )

        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.is_student = validated_data.get('is_student', instance.is_student)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance

    def to_representation(self, instance):
        return { 'id': instance.id }

    class Meta:
        model = Election
        fields = ('id', 'date_start', 'date_end', 'is_student', 'name', 'candidates', 'description')


class AdminCandidateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('id', 'name', 'surname', 'is_student', 'annotation')


class AdminCandidateReadSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'is_student': instance.is_student,
            'name': instance.name,
            'surname': instance.surname,
            'annotation': instance.annotation,
            'elections': [
                {
                    'id': election.id,
                    'date_start': election.date_start,
                    'date_end': election.date_end,
                    'is_student': election.is_student,
                    'name': election.name,
                    'votes': Score.objects.filter(election=election).aggregate(votes_sum=functions.Coalesce(Sum('votes'), 0))['votes_sum'],
                    'candidates': [
                        {
                            'id': candidate.id,
                            'votes': votes,
                        } for candidate, votes in map(lambda x: (x.candidate, x.votes), Score.objects.filter(election=election))
                    ]
                } for election in map(lambda x: x.election, Score.objects.filter(candidate=instance))
            ],
        }

    def to_internal_value(self, data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class ElectionGetResultsSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        response = {
            'id': instance.id,
            'date_start': instance.date_start,
            'date_end': instance.date_end,
            'is_student': instance.is_student,
            'name': instance.name,
            'description': instance.description,
        }
        if instance.date_end <= datetime.datetime.now(tz):
            total_votes = 0
            for score in Score.objects.filter(election=instance):
                total_votes += score.votes;
            response['candidates'] = []
            for score in Score.objects.filter(election=instance).order_by('-votes'):
                cand = {
                    'id': score.candidate.id,
                    'name': score.candidate.name,
                    'surname': score.candidate.surname,
                    'is_student': score.candidate.is_student,
                    'annotation': score.candidate.annotation,
                    }
                if total_votes != 0:
                    cand['percentage'] = score.votes / total_votes
                response['candidates'].append(cand)
        else:
            response['candidates'] = [
                {
                    'id': score.candidate.id,
                    'name': score.candidate.name,
                    'surname': score.candidate.surname,
                    'is_student': score.candidate.is_student,
                    'annotation': score.candidate.annotation,
                } for score in Score.objects.filter(election=instance)]
        return response

    def to_internal_value(self, data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError


class NotificationInfoSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):

        return {
            'election_id': instance.election.id,
            'votes_available': len(Vote.objects.filter(notification=instance))
        }

    def to_internal_value(self, data):

        raise NotImplementedError

    def update(self, instance, validated_data):

        raise NotImplementedError

    def create(self, validated_data):

        raise NotImplementedError


class AdminElectionWriteSerializer(serializers.ModelSerializer):
    candidates = serializers.PrimaryKeyRelatedField(queryset=Candidate.objects.all(), many=True)

    def create(self, validated_data):
        candidates_data = validated_data.pop('candidates')
        election = Election.objects.create(**validated_data)
        for candidate in candidates_data:
            Score.objects.create(
                candidate=candidate,
                election=election,
            )
        return election

    def update(self, instance, validated_data):
        candidates_data = validated_data.pop('candidates')
        for score in Score.objects.filter(election=instance):
            if score.candidate.id not in candidates_data:
                score.candidate.delete()

            candidates_data = list(filter(lambda x: x != score.candidate.id, candidates_data))

        for candidate in candidates_data:
            Score.objects.create(
                candidate=candidate,
                election=instance,
            )

        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.is_student = validated_data.get('is_student', instance.is_student)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance

    class Meta:
        model = Election
        fields = ('id', 'date_start', 'date_end', 'is_student', 'name', 'candidates', 'description')
