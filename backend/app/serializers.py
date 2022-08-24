from dataclasses import field
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ClubSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    class Meta:
        model = Club
        fields = ['id', 'name', 'category', 'intro']

    
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ManagerSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    user = UserSerializer()
    club = ClubSerializer(fields=('id', 'name'))
    class Meta:
        model = Manager
        fields = ['id', 'user', 'club', 'super']


class ApplySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    applier = UserSerializer(many=False, read_only=True)
    club_id = serializers.ReadOnlyField(source='recruit.club.pk')
    club_name = serializers.ReadOnlyField(source='recruit.club.name')
    deadline = serializers.ReadOnlyField(source='recruit.deadline')
    class Meta:
        model = Apply
        fields = ['id', 'applier', 'club_id', 'club_name', 'recruit', 'content', 'submit_at', 'temp_save', 'curr_step']



class RecruitSerializer(serializers.ModelSerializer):

    club = ClubSerializer(fields=('id', 'name', 'category'))

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    class Meta:
        model = Recruit
        fields = ['id', 'club', 'title', 'content', 'uploaded', 'deadline', 'total_step', 'in_progress']


class CommentSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(fields=('user'))

    class Meta:
        model = Comment
        fields = ['id', 'apply', 'content', 'line_idx', 'manager', 'uploaded']


class NoticeSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(fields=('user'))

    class Meta:
        model = Notice
        fields = ['id', 'club', 'content', 'view_range', 'manager', 'uploaded']


class ApplyFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForm
        fields = ['id', 'club', 'title', 'content']


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

class SelectTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectTime
        fields = '__all__'