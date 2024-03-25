from django.contrib import admin
from .models import Hastag,Post,PostVote

# Register your models here.
class PostInline(admin.TabularInline):
    model = Post.hastags.through
    extra = 1

class HashtagAdmin(admin.ModelAdmin):
    inlines = [
        PostInline,
    ]
    readonly_fields = ("id",)

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]

admin.site.register(Hastag,HashtagAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(PostVote)