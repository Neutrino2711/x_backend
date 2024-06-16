from rest_framework import serializers 
from post.models import (
    Post,
    Bookmark,
    PostVote,
    Hastag,
    # Comment,
    # CommentVote,
)
from user.serializers import UserSerializer



class PostCreateSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating a post
    '''

    '''
    defining a validator such that atleast one of these (content,image) should be there
    '''

  
            


    class Meta:
        model = Post 
        fields = ("content","image","parent")
        validators = []


class PostListSerializer(serializers.ModelSerializer):
    '''
    Serializer for listing all posts
    '''

    author = UserSerializer(read_only = True)

    score = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="post-detail",
        lookup_field = "pk",
        lookup_url_kwarg = "pk"

    )

    class Meta:
        model = Post 
        fields = "__all__"

    def get_score(self,obj):
        return obj.score()
    
    def get_vote(self,obj):
        user = self.context["request"].user
        vote = PostVote.objects.filter(post=obj,user=user).first()
        if vote:
            return vote.vote 
        return None 
    

class PostDetailSerializer(serializers.ModelSerializer):
    '''
    Serializer for listing all posts
    '''

    author = UserSerializer(read_only = True)

    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()


    class Meta:
        model = Post 
        fields = "__all__"

    def get_upvotes(self,obj):
        return obj.upvote()
    
    def get_downvotes(self,obj):
        return obj.downvotes()
    
    def get_score(self,obj):
        return obj.score()
    
    def get_is_bookmarked(self,obj):
        user = self.context["request"].user
        return Bookmark.objects.filter(post = obj,user =user).exists()
    
    def get_vote(self,obj):
        user = self.context["request"].user 
        vote = PostVote.objects.filter(post = obj,user =user).first()
        if vote: 
            return vote.vote 
        return None 

class HastagsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hastag
        fields = "__all__"

        



        # hastags  = serializers.SerializerMethodField()

        # def get_hashtags(self,object):
        #     return object.hastags

# class CommentListSerializer(serializers.ModelSerializer):


# class CommentListSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only = True)
     
    # upvotes = serializers.SerializerMethodField()
    # downvotes = serializers.SerializerMethodField()
    # score = serializers.SerializerMethodField()
    # vote = serializers.SerializerMethodField()

    # class Meta:
    #     model = Comment
    #     fields = "__all__"

    # def get_upvotes(self, obj):
    #     return obj.upvotes()

    # def get_downvotes(self, obj):
    #     return obj.downvotes()

    # def get_score(self, obj):
    #     return obj.score()
    
    # def get_vote(self,obj):
    #     user = self.context["request"].user 
    #     vote = CommentVote.objects.filter(comment= obj,user = user).first()
    #     if vote:
    #         return vote.vote 
    #     return None 