from posts.models import Comment, Group, Post, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'posts', 'comments')
        ref_name = 'ReadOnlyUsers'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(
        source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'post', 'created')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(
        source='author.username', read_only=True,
        default=serializers.CurrentUserDefault())
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image',
                  'group', 'pub_date', 'comments')


class GroupSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', 'posts')
        read_only_field = ('id', 'title', 'slug', 'description', 'posts')

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                'Имя не может совпадать с описанием!')
        return data
