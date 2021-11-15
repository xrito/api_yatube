from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# import datetime as dt

from posts.models import Group, Post, Comment, User


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)  # рабочий!
    comments = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)  # рабочий!

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'posts', 'comments')
        ref_name = 'ReadOnlyUsers'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # рабочий!

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'post', 'created')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(
        source='author.username', default=serializers.CurrentUserDefault(),
        read_only=True)  # рабочий!
    group = serializers.StringRelatedField(read_only=True)  # рабочий!
    comments = CommentSerializer(many=True, required=False)  # рабочий!

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image',
                  'group', 'pub_date', 'comments')
        read_only_fields = ('author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Post.objects.all(),
                fields=('text', 'author')
            )
        ]

    # def validate_birth_year(self, value):
    #     year = dt.date.today().year
    #     if not (year - 40 < value <= year):
    #         raise serializers.ValidationError('Проверьте год рождения!')
    #     return value

    # def get_age(self, obj):
    #     return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
        if 'comments' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post
        else:
            comments = validated_data.pop('comments')
            post = Post.objects.create(**validated_data)
            for comment in comments:
                current_comment, status = Comment.objects.get_or_create(
                    **comment)
                Comment.objects.create(
                    comment=current_comment, post=post)
            return post


class GroupSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(
        many=True, read_only=True)  # рабочий!

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', 'posts')
        read_only_field = ('id', 'title', 'slug', 'description', 'posts')

    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError(
                'Имя не может совпадать с описанием!')
        return data
