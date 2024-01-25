from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Post, Comment
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import CommentSerializer, PostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.response import Response
# from cacheops import cached_view_as, cached_as

# share post not yet...


# create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post_api_view(request):
    user = request.user
    post_data = request.data

    try:
        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# show list and search posts for title and body. This searching code not yet over.
class PostAPiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ['id', 'title', "body"]
    search_fields = ['title', 'body']
    # tahlil


# post detail
class PostDetailApiView(APIView):

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"message": "Post Not Found.!"})

        serializer = PostSerializer(post)

        return Response(serializer.data)


# get your posts
@cache_page(60*10)
@api_view(['GET'])
def get_post(request):
    if request.user.is_authenticated:
        post = Post.objects.filter(created_by=request.user)

        if post:
            serializer = PostSerializer(post, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "You have not any posts...!"}, status=status.HTTP_404_NOT_FOUND)
    else:
        Response({"error": "User is not authenticated.!"}, status=status.HTTP_401_UNAUTHORIZED)


# update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    try:
        post = Post.objects.get(pk=pk, created_by=request.user)

    except Post.DoesNotExist:
        return Response({"error": "Post Not Found.!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete post
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk, created_by=request.user)
        post.delete()
        return Response({"message": "Post Successfully Deleted.!"})

    except Post.DoesNotExist:
        return Response({"error": "Post Not Found.!"}, status=status.HTTP_404_NOT_FOUND)


# views for comment
class CreateCommentApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                post = Post.objects.get(pk=pk)
                serializer.save(created_by=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Post.DoesNotExist:
                return Response({"error": "Post Not Found.!"}, status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as i:
                return Response({"error": str([i])})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# comment list
class CommentsListApiView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return cache_page(60 * 15)(view)


# update comment
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk, created_by=request.user)

    except Comment.DoesNotExist:
        return Response({"error": "Comment Not Found.!"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(comment, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete comment


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk, created_by=request.user)

    except Comment.DoesNotExist:
        return Response({"error": "Comment Not Found.!"}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()

    return Response({"message": "Comment Successfully Deleted.!"}, status=status.HTTP_200_OK)


# like and dislike for posts

class LikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.like.add(request.user)
        post.dislike.remove(request.user)
        post.save()
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DislikeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.like.remove(request.user)
        post.dislike.add(request.user)
        post.save()
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)
