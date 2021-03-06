from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Userprofile, Posts, Postlike, Comments, Commentlike, Polls, PollVote

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = ["id", "user", "image", "get_proname", "get_proemail", "get_proimage", "get_totalquestions", "get_datejoined"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ["id", "title", "tags", "body", "thumbnail", "timestamp", "get_username", "get_userpic" , "author", "likecount", "commentcount",]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "body", "author", "posts", "timestamp", "thumbnail", "get_username", "get_userpic", "commentlike"]

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postlike
        fields = '__all__'

class CommentlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentlike
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polls
        fields = ["id", "question", "choice1", "choice2", "choice3", "choice4", "choice5", "choice1_total", "choice2_total", "choice3_total", "choice4_total", "choice5_total", "author", "completed", "timestamp", "total_users", "choice1_val", "choice2_val", "choice3_val", "choice4_val", "choice5_val", "choice1_wid", "choice2_wid", "choice3_wid", "choice4_wid", "choice5_wid", "get_username", "get_userpic", "total_response", "ends_by"]


