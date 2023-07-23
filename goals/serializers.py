from typing import Tuple
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.relations import SlugRelatedField
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from rest_framework.serializers import ModelSerializer, CurrentUserDefault, HiddenField, PrimaryKeyRelatedField,\
    ChoiceField
from core.serializers import ProfileSerializer
from core.models import User


class GoalCategoryCreateSerializer(ModelSerializer):
    """Serializer for creating a new category"""
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields: Tuple [str, ...] = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_board(self, value: Board) -> Board:
        if value.is_deleted:
            raise ValidationError("Board removed")
        if not BoardParticipant.objects.filter(
            board_id=value.id,
            user_id=self.context["request"].user.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists():
            raise PermissionDenied

        return value


class GoalCategorySerializer(ModelSerializer):
    """Serializer for retrieving/updating/deleting category"""
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields: Tuple [str, ...] = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(ModelSerializer):
    """Serializer for creating a new goal"""
    category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields: Tuple [str, ...] = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError('Category not found')

        if not BoardParticipant.objects.filter(
            board_id=value.board.id,
            user_id=self.context['request'].user.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ).exists():
            raise PermissionDenied

        return value


class GoalSerializer(ModelSerializer):
    """Serializer for retrieving/updating/deleting goal"""
    category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.filter(is_deleted=False))
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields: Tuple [str, ...] = ("id", "created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError('Category not found')
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value


class GoalCommentCreateSerializer(ModelSerializer):
    """Serializer for creating a new comment"""
    user = HiddenField(default=CurrentUserDefault())

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value

    class Meta:
        model = GoalComment
        read_only_fields: Tuple [str, ...] = ('id', 'user', 'created', 'updated')
        fields = '__all__'


class GoalCommentSerializer(ModelSerializer):
    """Serializer for retrieving/updating/deleting comment"""
    user = ProfileSerializer(read_only=True)
    goal = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields: Tuple [str, ...] = ('id', 'goal', 'user', 'created', 'updated')
        fields = '__all__'


class BoardCreateSerializer(ModelSerializer):
    """Serializer for creating a new board"""
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields: Tuple [str, ...] = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data: dict) -> Board:
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(ModelSerializer):
    """Serializer for participants"""
    role = ChoiceField(
        required=True, choices=BoardParticipant.Role.choices[1:]
    )
    user = SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields: Tuple [str, ...] = ("id", "created", "updated", "board")


class BoardSerializer(ModelSerializer):
    """Serializer for retrieving/updating/deleting board"""
    participants = BoardParticipantSerializer(many=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields: Tuple [str, ...] = ("id", "created", "updated")

    def update(self, instance: Board, validated_data: dict) -> Board:
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance


class BoardListSerializer(ModelSerializer):
    """Serializer for a list of boards"""
    class Meta:
        model = Board
        fields = "__all__"
