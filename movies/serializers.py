from rest_framework import serializers
from movies.models import Movie, MovieChoices, MovieOrder


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.CharField(max_length=50)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    rating = serializers.ChoiceField(
        choices=MovieChoices.choices, default=MovieChoices.G
    )
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.SerializerMethodField(read_only=True)

    def get_added_by(self, obj):
        return obj.user.email

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    title = serializers.SerializerMethodField(read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_by = serializers.SerializerMethodField(read_only=True)

    def get_buyed_by(self, obj):
        return obj.user.email

    def get_title(self, obj):
        return obj.movie.title

    def create(self, validated_data):
        price = validated_data.get("price")
        user = self.context["request"].user
        movie = Movie.objects.get(id=self.context["movie_id"])

        movie_order = MovieOrder.objects.create(user=user, movie=movie, price=price)
        return movie_order
