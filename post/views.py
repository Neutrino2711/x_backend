from rest_framework import generics, permissions, authentication 
from rest_framework.response import Response 
from django.db.models import Count,Q 
from post.models import (
    Post,
    Bookmark,
    PostVote,
    Hastag,
    # Comment,
    # CommentVote,
)
from post.serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    HastagsListSerializer,
    # CommentListSerializer,
)



# Create your views here.

class ListCreatePostView(generics.ListCreateAPIView):
    '''
    Create a new post
    '''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer
    
    def perform_create(self,serializer):
        serializer.save(author = self.request.user)


class RetrieveUpdateDestroyPostView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, Update or Delete a post
    '''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class BookmarkView(generics.GenericAPIView):
    '''
    View to bookmark or remove a bookmark of the authenticated user
    '''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self,request,pk):
        post = generics.get_object_or_404(Post,pk =pk)
        bookmark,created = Bookmark.objects.get_or_create(user = request.user,post = post)
        #The get or created returns a tuple where tuple.first is Bookmark object and tuple.second is boolean indicating whether the object was created(True) or retrieved 
        if not created: 
            bookmark.delete()
        return Response({"success":True})
    

class PostVoteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    # what is this doing
    def post(self,request,pk):
        post = generics.get_object_or_404(Post,pk=pk)
        vote = int(request.data.get("vote"))
        if vote not in [PostVote.UPVOTE,PostVote.DOWNVOTE]:
            return Response({"success":False})
        post_vote,created = PostVote.objects.get_or_create(
            user = request.user,post = post,defaults = {"vote":vote}

        )
        if not created: 
            if post_vote.vote == vote:
                post_vote.delete()

            else:
                post_vote.vote = vote 
                post_vote.save()
        else: 
            post_vote.vote = vote
            post_vote.save()
        return Response({"success":True})
    

class UserPostListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user)


class UserBookmarkListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    serializer_class = PostListSerializer

    def get_queryset(self):
        user = self.request.user
        bookmarks = Bookmark.objects.filter(user = user)
        return Post.objects.filter(bookmarks__in = bookmarks)
    

class TrendingHastagsView(generics.ListAPIView):
    serializer_class = HastagsListSerializer

    def get_queryset(self):
        return Hastag.objects.annotate(posts_count=Count('posts')).order_by('-posts_count').filter()