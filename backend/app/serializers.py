from dataclasses import field
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ClubSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Club
        fields = ['id', 'name', 'category', 'intro']
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class ManagerSerializer(serializers.ModelSerializer):
    club_id = serializers.ReadOnlyField(source='club.pk')
    club_name = serializers.ReadOnlyField(source='club.name')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Manager
        fields = ['id', 'club_id', 'club_name', 'username', 'email', 'super']


class ApplySerializer(serializers.ModelSerializer):
    applier = UserSerializer(many=False, read_only=True)
    club_id = serializers.ReadOnlyField(source='recruit.club.pk')
    

    class Meta:
        model = Apply
        fields = ['id', 'applier', 'club_id', 'recruit', 'content', 'submit_at', 'temp_save', 'curr_step']


class RecruitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recruit
        fields = ['id', 'club', 'title', 'content', 'uploaded', 'deadline', 'total_step']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'manager', 'apply', 'content', 'uploaded', 'line_idx']


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

class SelectTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectTime
        fields = '__all__'