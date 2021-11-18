from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField

from posts.models import Comment, Group, Post, User


class UserSerializer(serializers.ModelSerializer):
    posts = SlugRelatedField(
        many=True, read_only=True, slug_field='posts')

    class Meta:
        model = User
        fields = '__all__'
        ref_name = 'ReadOnlyUsers'


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                'Имя не может совпадать с описанием!')
        return data
