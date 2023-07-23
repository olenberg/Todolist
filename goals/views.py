from django.db import transaction
from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer,\
    GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardParticipantSerializer, \
    BoardSerializer, BoardListSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from goals.filters import GoalDateFilter
from goals.permissions import GoalCategoryPermission, GoalPermission, CommentPermission, BoardPermission
from rest_framework.permissions import IsAuthenticated


class GoalCategoryCreateView(CreateAPIView):
    """API endpoint for creating a new category"""
    model = GoalCategory
    permission_classes: list = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """API endpoint for retrieving a list of categories"""
    model = GoalCategory
    permission_classes: list = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    ordering_fields: list[str, ...] = ["title", "created"]
    ordering: list[str, ...] = ["title"]
    search_fields: list[str, ...] = ["title"]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.filter(board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving/updating/deleting a category"""
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes: list = [GoalCategoryPermission]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        return GoalCategory.objects.filter(board__participants__user=self.request.user).exclude(is_deleted=True)

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):
    """API endpoint for creating a new goal"""
    model = Goal
    permission_classes: list = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """API endpoint for retrieving a list of goals"""
    model = Goal
    permission_classes: list = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends: list = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GoalDateFilter
    search_fields: list[str, ...] = ["title", "description"]
    ordering_fields: list[str, ...] = ["priority", "due_date"]
    ordering: list[str, ...] = ["priority", "due_date"]

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.filter(category__board__participants__user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving/updating/deleting a goal"""
    model = Goal
    permission_classes: list = [GoalPermission]
    serializer_class = GoalSerializer

    def get_queryset(self) -> QuerySet[Goal]:
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(CreateAPIView):
    """API endpoint for creating a new comment"""
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes: list = [IsAuthenticated]


class GoalCommentListView(ListAPIView):
    """API endpoint for retrieving a list of comments"""
    serializer_class = GoalCommentSerializer
    permission_classes: list = [IsAuthenticated]
    # pagination_class = LimitOffsetPagination
    filter_backends: list = [OrderingFilter, DjangoFilterBackend]
    # ordering_fields = ["text", "created"]
    filterset_fields = ['goal']
    ordering = ["-created"]

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving/updating/deleting a comment"""
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes: list = [CommentPermission]

    def get_queryset(self) -> QuerySet[GoalComment]:
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user)


class BoardCreateView(CreateAPIView):
    """API endpoint for creating a new board"""
    model = Board
    permission_classes: list = [BoardPermission]
    serializer_class = BoardCreateSerializer


class BoardListView(ListAPIView):
    """API endpoint for retrieving a list of boards"""
    model = Board
    permission_classes: list = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = BoardListSerializer
    filter_backends: list = [OrderingFilter]
    ordering: list[str] = ["title"]

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving/updating/deleting a board"""
    model = Board
    serializer_class = BoardSerializer
    permission_classes: list = [BoardPermission]

    def get_queryset(self) -> QuerySet[Board]:
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
