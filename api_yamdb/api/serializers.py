from rest_framework import serializers

from reviews.models import (Category, Comment, Genre,
                            GenreTitle, Review, Title, User)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        source='review__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'category', 'genre', 'description', 'rating'
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')

    def create(self, validated_data):
        genres = validated_data.pop('genre')

        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.create(
                genre=genre, title=title)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        if self.context["request"].method == "POST":
            user = self.context["request"].user
            title_id = self.context["view"].kwargs.get("title_id")
            if Review.objects.filter(
                author_id=user.id, title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    "Вы не можете оставить отзыв дважды! :)"
                )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Оценку можно поставить только от 1 до 10"
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Пользователю нельза задавать имя me'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value):
            raise serializers.ValidationError(
                'Такой Email уже зарегистрирован'
            )
        return value


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    token = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', 'token',)
        read_only_fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class NotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)
