from django.db import models
from django.contrib.auth.models import User
import datetime


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='proimages',
                              default='default.png', blank=True, null=False)

    def get_proname(self):
        return self.user.username

    def get_proemail(self):
        return self.user.email

    def get_proimage(self):
        return self.image.url

    def get_totalquestions(self):
        return self.posts_set.count()

    def get_datejoined(self):
        return self.user.date_joined


class Posts(models.Model):
    title = models.CharField(null=False, max_length=50)
    tags = models.CharField(null=False, max_length=50)
    body = models.TextField(null=False)
    author = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    thumbnail = models.ImageField(
        upload_to='postimages', blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_username(self):
        return self.author.user.username

    def get_userpic(self):
        return self.author.image.url

    def likecount(self):
        return self.postlike_set.count()

    def commentcount(self):
        return self.comments_set.count()


class Comments(models.Model):
    body = models.TextField(null=False)
    author = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(
        upload_to='commentimages', blank=True, null=False)

    def get_username(self):
        return self.author.user.username

    def get_userpic(self):
        return self.author.image.url

    def commentlike(self):
        return self.commentlike_set.count()

    def commentcount(self):
        return self.comments_set.count()

class Postlike(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'post'),)
        index_together = (('user', 'post'),)


class Commentlike(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'comment'),)
        index_together = (('user', 'comment'),)

class Polls(models.Model):
    question = models.TextField(null=False)
    choice1 = models.CharField(max_length=50,null=False)
    choice2 = models.CharField(max_length=50,null=False)
    choice3 = models.CharField(max_length=50,blank=True)
    choice4 = models.CharField(max_length=50,blank=True)
    choice5 = models.CharField(max_length=50,blank=True)
    choice1_total = models.IntegerField(null=False,default=0)
    choice2_total = models.IntegerField(null=False,default=0)
    choice3_total = models.IntegerField(null=False, default=0)
    choice4_total = models.IntegerField(null=False, default=0)
    choice5_total = models.IntegerField(null=False, default=0)
    author = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_username(self):
        return self.author.user.username

    def get_userpic(self):
        return self.author.image.url

    def ends_by(self):
        return self.timestamp + datetime.timedelta(days=1)

    def total_users(self):
        return Userprofile.objects.all().count() -1 

    def choice1_val(self):
        return round((self.choice1_total / self.total_users())*100,2)
    
    def choice2_val(self):
        return round((self.choice2_total / self.total_users())*100,2)
    
    def choice3_val(self):
        return round((self.choice3_total / self.total_users())*100,2)
    
    def choice4_val(self):
        return round((self.choice4_total / self.total_users())*100,2)
    
    def choice5_val(self):
        return round((self.choice5_total / self.total_users())*100,2)

    def choice1_wid(self):
        return int(100 - ((self.choice1_total / self.total_users())*100))
    
    def choice2_wid(self):
        return int(100 - ((self.choice2_total / self.total_users())*100))
    
    def choice3_wid(self):
        return int(100 - ((self.choice3_total / self.total_users())*100))
    
    def choice4_wid(self):
        return int(100 - ((self.choice4_total / self.total_users())*100))
    
    def choice5_wid(self):
        return int(100 - ((self.choice5_total / self.total_users())*100))
    
    def total_response(self):
        return int(self.choice1_total + self.choice2_total + self.choice3_total + self.choice4_total + self.choice5_total)
    
class PollVote(models.Model):
    user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'poll'),)
        index_together = (('user', 'poll'),)