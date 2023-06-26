from rest_framework.exceptions import PermissionDenied, ValidationError
from goals.models import GoalCategory, Goal, GoalComment
from rest_framework.serializers import ModelSerializer, CurrentUserDefault, HiddenField, PrimaryKeyRelatedField
from core.serializers import ProfileSerializer


class GoalCategoryCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, category):
        if category.is_deleted:
            raise ValidationError("Category not found")

        if category.user != self.context["request"].user:
            raise PermissionDenied

        return category


class GoalSerializer(ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError('Goal not found')
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'user', 'created', 'updated')
        fields = '__all__'


class GoalCommentSerializer(ModelSerializer):
    user = ProfileSerializer(read_only=True)
    goal = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalComment
        read_only_fields = ('id', 'goal', 'user', 'created', 'updated')
        fields = '__all__'
