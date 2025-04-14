from django.urls import path, include
from .views import PostAPiView, create_post_api_view, get_post, update_post, delete_post, \
    CreateCommentApiView, CommentsListApiView, update_comment, delete_comment, LikeApiView, \
    DislikeApiView, PostDetailApiView, \
    create_channel, get_channel, delete_channel, ListChannelApiView
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r"post", PostViewSet, basename='post')

urlpatterns = [
    # url for posts
    path('create_post/', create_post_api_view, ),
    path('posts/', PostAPiView.as_view(), ),
    path('post_detail/<int:pk>/', PostDetailApiView.as_view(), ),
    path('get_my_posts/', get_post, ),
    path('update_post/<int:pk>/', update_post, ),
    path('delete/<int:pk>/', delete_post, ),
    # url Like And Dislike for posts
    path('post/<int:pk>/like/', LikeApiView.as_view(), name='like'),
    path('post/<int:pk>/dislike/', DislikeApiView.as_view(), name='dislike'),
    # url for comment
    path('create_comment/<int:pk>/', CreateCommentApiView.as_view(), ),
    path('comment_list/', CommentsListApiView.as_view(), name='create_comment'),
    path('update_comment/<int:pk>/', update_comment, ),
    path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),
    # urls for channel
    path('create_channel/', create_channel, ),
    path('get_channel/<int:pk>/', get_channel, ),
    path('delete_channel/<int:pk>/', delete_channel, ),
    path('channels/', ListChannelApiView.as_view(), ),







]

