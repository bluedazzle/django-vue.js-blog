from django.contrib import admin
from api.models import *
# Register your models here.

admin.site.register(Article)
admin.site.register(Classification)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Knowledge)
admin.site.register(Env)
admin.site.register(Collection)
