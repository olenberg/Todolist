from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.request import Request
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryPermission(IsAuthenticated):
    """
    Permission class for Category model,
    determines if a user has permission to access a category
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()


class GoalPermission(IsAuthenticated):
    """
    Permission class for Goal model,
    determines if a user has permission to access a goal
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists()


class CommentPermission(IsAuthenticated):
    """
    Permission class for Comment model,
    determines if a user has permission to access a comment
    """
    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalComment):
        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.goal.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer,
            ],
        ).exists()


class BoardPermission(IsAuthenticated):
    """
    Permission class for Board model,
    determines if a user has permission to access a board
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()
