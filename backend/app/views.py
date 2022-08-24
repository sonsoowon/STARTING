
from dataclasses import fields
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



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def my_manager_accounts(self, request, pk=None):
        user = self.get_object()
        manager_queryset = user.manager_accounts.all()
        serializer = ManagerSerializer(manager_queryset, many=True, fields=('id', 'club'))
        return Response(serializer.data)


    @action(detail=True)
    def my_applies(self, request, pk=None):
        user = self.get_object()
        apply_queryset = user.applies.all()
        serializer = ApplySerializer(apply_queryset, many=True, fields=('id', 'club_id', 'club_name', 'temp_save', 'deadline'))
        return Response(serializer.data)

class ClubViewSet(viewsets.ModelViewSet):

    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                        IsManagerOrReadOnly]


    def list(self, request):
        club_queryset = Club.objects.all()
        serializer = ClubSerializer(club_queryset, many=True, fields=('id', 'name', 'category'))

        return Response(serializer.data)

    @action(detail=True)
    def manager_index_page(self, request, pk=None):
        club = self.get_object()
        recruit_inprogress = Recruit.objects.get(club=club.pk, in_progress=True)
        total_applies = Apply.objects.filter(recruit=recruit_inprogress, temp_save=False).count()

        res = {
            'total_applies': total_applies,
            'recruit_inprogress': recruit_inprogress.pk,
        }

        return Response(res)


    # 코드를 어떻게 리팩토링 하지?

    
    @action(detail=True)
    def recruits(self, request, pk=None):
        club = self.get_object()
        recruit_queryset = club.recruits.all()
        serializer = RecruitSerializer(recruit_queryset, many=True, fields=('id', 'title', 'uploaded'))
        return Response(serializer.data)


    @action(detail=True)
    def managers(self, request, pk=None):
        club = self.get_object()
        manager_queryset = club.managers.all()
        serializer = ManagerSerializer(manager_queryset, many=True, fields=('id', 'user', 'super'))
        return Response(serializer.data)


    @action(detail=True)
    def notices(self, request, pk=None):
        club = self.get_object()
        notice_queryset = club.notices.all()
        serializer = NoticeSerializer(notice_queryset, many=True)
        return Response(serializer.data) 

class RecruitViewSet(viewsets.ModelViewSet):

    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer

    #permission_classes = [IsManagerOrReadOnly]
    # 운영진만 list_applies, get_apply_count GET 가능

    def list(self, request):
        recruit_queryset = Recruit.objects.all()
        serializer = RecruitSerializer(recruit_queryset, many=True, fields=('id', 'club', 'title', 'deadline', 'uploaded'))
        
        return Response(serializer.data)
    
    @action(detail=True)
    def applies(self, request, pk=None):
        recruit = self.get_object()
        apply_queryset = recruit.appliers.filter(temp_save=False)
        serializer = ApplySerializer(apply_queryset, many=True, fields=('id', 'applier', 'submit_at', 'curr_step'))
        return Response(serializer.data)


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class ApplyViewSet(viewsets.ModelViewSet):

    queryset = Apply.objects.all()
    serializer_class = ApplySerializer

    # 운영진만 list_comment GET 가능
    @action(detail=True)
    def comments(self, request, pk=None):
        apply = self.get_object()
        comment_queryset = apply.comments.all()
        serializer = CommentSerializer(comment_queryset, many=True)
        return Response(serializer.data)


# 운영진만 POST, GET 가능
# 특정 comment에 대해 작성자만 PUT, DELETE 가능
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# view_range 에 따라 GET 범위 변화
# 운영진만 POST, DELETE 가능
# PUT 불가능
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer


class SelectTimeViewSet(viewsets.ModelViewSet):
    queryset = SelectTime.objects.all()
    serializer_class = SelectTimeSerializer


class ApplyFormViewSet(viewsets.ModelViewSet):
    pass