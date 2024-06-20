from django.db import models

from io import BytesIO 
from PIL import Image 
import os 
from django.core.exceptions import ValidationError


# supabase
# from supabase import create_client,Client

from django.core.files.base import ContentFile 
from django.conf import settings 
from django.db.models import Count,Case,When,IntegerField 
import re 


# supabase
# url: str = settings.SUPABASE_URL
# url: str = settings.SUPABASE_KEY
# supabase: Client = create_client(url,key)
# bucket_name: str = "post_images"

# Create your models here.

class Hastag(models.Model):
    name = models.CharField(max_length = 100,unique = True)

    def __str__(self):
        return self.name
    
    # def get_or_create(self,name):
    #     super().save(name = name)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        


class Post(models.Model):

    

    content = models.TextField(blank = True)
    hastags = models.ManyToManyField(Hastag,blank = True,related_name= "posts")
    image = models.ImageField(null = True,blank = True)
    def clean(self):
        if not self.content and not self.image:
            raise ValidationError("Either content or image is required.")

        # Always return cleaned data
        return super().clean()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    author = models.ForeignKey("user.User",on_delete = models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete = models.CASCADE,
        related_name = "replies",
        null = True,
        blank = True,

    )
    depth = models.PositiveIntegerField(default = 0)

    def upvote(self) -> int:
        return self.votes.filter(vote = PostVote.UPVOTE).count()
    

    def downvotes(self): 
        return self.votes.filter(vote= PostVote.DOWNVOTE).count()
    
    def score(self):
        upvotes = self.votes.filter(vote = PostVote.UPVOTE).count()
        downvotes = self.votes.filter(vote = PostVote.DOWNVOTE).count()
        return upvotes-downvotes 
    
    def comment(self,post):
        self.replies.add(post)

    def save(self,*args,**kwargs ):
        old_image = None 
        if self.pk:
            old_image = Post.objects.get(pk = self.pk).image 

            if old_image and old_image != self.image:
                file_name = os.path.basename(old_image.name)
                # response = supabase.storage.from_(bucket_name).remove(file_name)

            if self.image and (not self.pk or self.image != old_image):
                #Open the uploaded image with Pillow 
                img = Image.open(self.image)

                #Convert the image mode to RGB 
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Compress the image to limit its size to 1MB
                output = BytesIO()
                img.save(output, format = "JPEG",quality = 60)

                # Upload the compressed image to Supabase Storage 
                # file_name = f"{self.image.name.split('.')[0]}.jpg"
                # file_content = ContentFile(output.read())
                # file_options = {
                #     "contentType": "image/jpeg",
                # }
                # response = supabase.storage.from_(bucket_name).upload(
                #     file = output.getvalue(), file_options = file_options,path = file_name
                # )
                # self.image = f"{bucket_name}/{file_name}"
        if self.parent is not None:
            self.depth = self.parent.depth + 1
        self.clean()
        super().save(*args,**kwargs)
        hastags = re.findall(r"#(\w+)",self.content)
        print(hastags)
        for hashtag in hastags:
            tag, created = Hastag.objects.get_or_create(name=hashtag)
            tag.save()
            # print(self.hastags)
            self.hastags.add(tag)  # Add the hashtag to the post's hashtags field
            # tag.posts.add(self)  # Add the post to the hashtag's posts field
        
        # super().save(*args,**kwargs)
        # print(f"Post saved with hashtags: {self.hastags.all()}")
        # if self.content is None and self.image is None:
        #     return 
        # else:    
        #     self.clean()
        #     super().save(*args,**kwargs)

    def __str__(self):
        return self.content
        

class Bookmark(models.Model):
    user = models.ForeignKey( 
        "user.User",on_delete= models.CASCADE,related_name = "bookmarks"
    )
    post = models.ForeignKey(
        "post.Post",
        on_delete= models.CASCADE,
        related_name = "bookmarks",

    )

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta: 
        unique_together = ("user","post")

    
    def __str__(self):
        return f"{self.user} - {self.post}"


class PostVote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE,"Upvote"),
        (DOWNVOTE,"Downvote"),
    )

    user = models.ForeignKey(
        "user.User", on_delete = models.CASCADE, related_name = "votes"

    )

    post = models.ForeignKey(
        "post.Post", on_delete = models.CASCADE, related_name = "votes"
    )
    vote = models.SmallIntegerField(choices = VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)


    class Meta:
        unique_together = ("user","post")


    def __str__(self):
        return f"{self.user} {self.get_vote_display()}d {self.post}" 
    
