
from django.shortcuts import render

from .serializers import *
from .models import *
from django.contrib.auth.models import User
from rest_framework import mixins, generics, viewsets
from rest_framework import serializers, permissions
from .permissions import *

from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response


# Create your views here.

"""
1. Club 가입 / 세부 정보 조회 및 수정

2. Manager 계정 추가 및 삭제


3. Recruit CRUD

4. Apply 조회 및 step 수정

5. Comment CRUD

6. ApplyForm CRUD

7. Notice 작성 및 삭제

8. TimeTable 작성 및 삭제

9. SelectTime 조회 및 fixed 수정

"""



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def list_manager_accounts(self, request, pk=None):
        user = self.get_object()
        manager_queryset = user.manager_accounts.all()
        serializer = ManagerSerializer(manager_queryset, many=True)
        return Response(serializer.data)




class ClubViewSet(viewsets.ModelViewSet):
    """
    <Club>
    GET(list, detail) : AllowAny 
    POST(create) : IsAuthenticated (only registered user) 
    PUT(update), DELETE(delete) : IsManagerOrReadOnly (only manager)

    """

    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsManagerOrReadOnly]


    """
    <Recruit>
    GET(list) : AllowAny

    """

    @action(detail=True)
    def list_recruits(self, request, pk=None):
        club = self.get_object()
        recruit_queryset = club.recruits.all()
        serializer = RecruitSerializer(recruit_queryset, many=True)
        return Response(serializer.data)



    @action(detail=True)
    def list_managers(self, request, pk=None):
        club = self.get_object()
        manager_queryset = club.managers.all()
        serializer = ManagerSerializer(manager_queryset, many=True)
        return Response(serializer.data)


    @action(detail=True)
    def list_notices(self, request, pk=None):
        club = self.get_object()
        notice_queryset = club.notices.all()
        serializer = NoticeSerializer(notice_queryset, many=True)
        return Response(serializer.data)


class RecruitViewSet(viewsets.ModelViewSet):

    """
    <Recruit>
    GET(list, detail) : AllowAny
    POST(create), PUT(update), DELETE(delete) : only Manager

    """

    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer

    #permission_classes = [IsManagerOrReadOnly]

    """
    <Apply>
    GET(list) : only Manager

    """

    @action(detail=True)
    def list_applies(self, request, pk=None):
        recruit = self.get_object()
        apply_queryset = recruit.appliers.all()
        serializer = ApplySerializer(apply_queryset, many=True)
        return Response(serializer.data)


    def get_apply_count(self, request, pk=None):
        recruit = self.get_object()
        apply_count = recruit.appliers.all.count()
        return apply_count


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer



class ApplyViewSet(viewsets.ModelViewSet):

    """
    <Apply>
    GET(detail) : temp_save=True - only applier / temp_save=False(최종 제출) - manager and applier
    POST(create) : IsAuthenticated (only registered user)
    PUT(update), DELETE(delete) : only applier with temp_save=True

    임시 저장이 아닌 최종 제출한 Apply instance 에 대해선 GET(detail, list) 만 가능하다

    """
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer



    @action(detail=True)
    def list_comments(self, request, pk=None):
        apply = self.get_object()
        comment_queryset = apply.comments.all()
        serializer = CommentSerializer(comment_queryset, many=True)
        return Response(serializer.data)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer


class SelectTimeViewSet(viewsets.ModelViewSet):
    queryset = SelectTime.objects.all()
    serializer_class = SelectTimeSerializer