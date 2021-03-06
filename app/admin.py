from django.contrib import admin
from .models import Userprofile, Posts, Comments, Polls, PollVote, Postlike, Commentlike
# Register your models here.
admin.site.register(Userprofile)
admin.site.register(Posts)
admin.site.register(Polls)
admin.site.register(Comments)
admin.site.register(PollVote)
admin.site.register(Postlike)
admin.site.register(Commentlike)