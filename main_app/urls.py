from django.urls import path
from . import views
from .views import LikeView, UnlikeView, SearchPost

urlpatterns = [
    
    #HOME 
    path('', views.home, name="home"), #in views folder use home view
    path('oldest', views.home_oldest, name="home_oldest"),
    path('likes', views.home_likes, name="home_likes"),
    
    #POSTs
    path('posts/create', views.PostCreate.as_view(), name="post_create"),
    path('posts', views.posts_index, name="posts_index"),
    path('posts/likes', views.posts_index_likes, name="posts_index_likes"),
    path('posts/oldest', views.posts_index_oldest, name="posts_index_oldest"),
    path('posts/user', views.user_posts_index, name="user_posts_index"),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name="post_update"),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name="post_delete"),
    path('posts/<int:pk>/', views.detail, name='post_detail'),
    path('posts/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    path('posts/search/', views.SearchPost, name='search_post'),
    path('like/<int:pk>/', views.LikeView, name='like_post'),
    path('unlike/<int:pk>/', views.UnlikeView, name='unlike_post'),
    
    
    #COMMENTS
    path('post/<int:pk>/comment/', views.CommentCreate.as_view(), name='comment_create'),
    path('post/<int:pk>/comment/update/', views.CommentUpdate.as_view(), name="comment_update"),   
    path('post/<int:pk>/comment/delete/', views.CommentDelete.as_view(), name="comment_delete"),
    
    #URL path for signup
    path('account/signup',views.signup,name='signup'),
    path('account/edit_profile/',views.edit_profile,name='edit_profile'),

    #ACCOUNT
    path('profile/', views.profile, name='profile'),
    
    ]   