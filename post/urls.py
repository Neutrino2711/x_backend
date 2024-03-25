from django.urls import path 
from post import views 

urlpatterns = [
    path("",views.ListCreatePostView.as_view(),name = "list-create",),
    path("user_posts/",views.UserPostListView.as_view(),name = "user-post"),
    path("user_bookmarks/",views.UserBookmarkListView.as_view(),name="user-bookmarks"),
    path("<int:pk>/",views.RetrieveUpdateDestroyPostView.as_view(),name = "post-detail"),
    path("<int:pk>/bookmark/",views.BookmarkView.as_view(),name = "bookmark"),
    path("<int:pk>/vote/",views.PostVoteView.as_view(),name="vote"),
    path("trending/",views.TrendingHastagsView.as_view(),name = "trending"),
    
]