from rest_framework.views import APIView, status, Request
from movies.models import Movie
from movies.serializers import MovieOrderSerializer, MovieSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from kenzie_buster.pagination import CustomPageNumberPagination


class MoviesView(APIView, CustomPageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request):
        movies = Movie.objects.get_queryset().order_by("id")

        pages = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(pages, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = Movie.objects.get(pk=movie_id)

        serializer = MovieSerializer(instance=movie, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = Movie.objects.get(pk=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        serializer = MovieOrderSerializer(
            data=request.data, context={"request": request, "movie_id": movie_id}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie, user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
