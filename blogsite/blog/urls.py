from django.urls import path,include
from . import views
app_name ='blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='post_list'),
    path('users/',views.UserListView.as_view(),name='user_list'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('post/create/',views.PostCreateView,name='post_create'),
    path('post/<pk>/update/',views.PostUpdateView.as_view(),name='post_update'),
    path('post/<pk>/delete/',views.PostDeleteView.as_view(),name='post_delete'),
    path('post/<pk>/', views.PostDetailView,name='post_detail'),
    path('comment/<pk>/update/',views.CommentUpdateView.as_view(),name='comment_update'),
    path('comment/<pk>/delete/',views.delete_comment_view,name='comment_delete'),
    path('successsignup/',views.SuccessSignUp,name='sign_up_success'),
    path('user/<pk>/',views.UserDetailView.as_view(),name='user_details'),
    path('block/<pk>',views.BlockUser,name='block_user'),
    path('unblock/<pk>',views.UnblockUser,name='unblock_user'),



]