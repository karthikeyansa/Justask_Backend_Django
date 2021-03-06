from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import ProfileSerializer, PostSerializer, CommentSerializer, PollSerializer

from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Userprofile, Posts, Comments, Postlike, Commentlike, Polls, PollVote

from better_profanity import profanity

from bs4 import BeautifulSoup
import requests

profanity.load_censor_words()


def checkprofile(request):
    try:
        profileuser = get_object_or_404(Userprofile, user=request.user)
    except:
        profileuser = Userprofile.objects.create(user=request.user)
    return profileuser


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class ProfileViewset(viewsets.ModelViewSet):
    queryset = Userprofile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

# http://127.0.0.1:8000/api/profiles/pictureupdate/

    @action(detail=False, methods=['PUT'], url_path="pictureupdate")
    def pictureUpdate(self, request, *args, **kwargs):
        profileuser = checkprofile(request)
        if 'image' in request.data:
            profileuser.image = request.data['image']
            profileuser.save()
            serializer = ProfileSerializer(profileuser, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Serialization Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)

# http://127.0.0.1:8000/api/profiles/picturedelete/

    @action(detail=False, methods=['DELETE'], url_path="picturedelete")
    def pictureDelete(self, request, *args, **kwargs):
        profileuser = checkprofile(request)
        if profileuser.image != 'default.png':
            profileuser.image = 'default.png'
            profileuser.save()
            serializer = ProfileSerializer(profileuser, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Picture Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=False, methods=['GET'], url_path="curuser")
    def curuser(self, request, *args, **kwargs):
        profileuser = checkprofile(request)
        serializer = ProfileSerializer(profileuser, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewset(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

# http://127.0.0.1:8000/api/posts/newpost/

    @action(detail=False, methods=['POST'], url_path="newpost")
    def newPost(self, request, *args, **kwargs):
        profileuser = checkprofile(request)
        if 'title' and 'tags' and 'body' in request.data:
            if 'thumbnail' in request.data:
                post = Posts.objects.create(title=profanity.censor(request.data['title']), tags=profanity.censor(request.data['tags']), body=profanity.censor(request.data['body']), thumbnail=request.data['thumbnail'], author=profileuser)
            if not 'thumbnail' in request.data:
                post = Posts.objects.create(title=profanity.censor(request.data['title']), tags=profanity.censor(request.data['tags']), body=profanity.censor(request.data['body']), author=profileuser)
            '''
            searchtext = post.title + '+stack+overflow'
            mainsite = f"https://www.google.com/search?&q={searchtext}"
            mainresponse = requests.get(mainsite)
            source = BeautifulSoup(mainresponse.text, "html.parser")
            maindiv = source.find_all("div", class_="ZINbbc xpd O9g5cc uUPGi")
            maindiv = maindiv[1].div
            mainsf = maindiv.find("a")["href"]
            mainsf = mainsf.replace("/url?q=", "")
            secresponse = requests.get(mainsf)
            source2 = BeautifulSoup(secresponse.text, "html.parser")
            mainbar = source2.find("div", {"id": "answers"})
            accepted = mainbar.find("div", {"class": "answer accepted-answer"})
            answercell = accepted.find("div", class_="answercell post-layout--right").div
            answercell = str("<a href='")+str(mainsf)+str("' target='_blank'><u>View full source</u></a><br><br>")+"\n"+str(answercell)
            body = answercell
            body = body.replace("<a",'<u class="text-primary"><a')
            body = body.replace("a>","a></u>")
            comment = Comments.objects.create(body=body, posts=post, author=Userprofile.objects.get(pk=2))
            print("Answered")
            '''
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Serialization Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)

# http://127.0.0.1:8000/api/posts/<post_id>/

    def destroy(self, request, pk=None, *args, **kwargs):
        Posts.objects.get(id=pk).delete()
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/posts/<post_id>/

    def update(self, request, pk=None, title=None, tags=None, body=None, thumbnail=None, *args, **kwargs):
        post = get_object_or_404(Posts, pk=pk)
        if 'title' in request.data:
            post.title = profanity.censor(request.data['title'])
        if 'tags' in request.data:
            post.tags = profanity.censor(request.data['tags'])
        if 'body' in request.data:
            post.body = profanity.censor(request.data['body'])
        if 'thumbnail' in request.data:
            post.thumbnail = request.data['thumbnail']
        post.save()
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/posts/
# all posts
    def list(self, request, *args, **kwargs):
        posts = Posts.objects.all().order_by('-timestamp')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/posts/myposts/
# user posts
    @action(detail=False, url_path="myposts")
    def userPosts(self, request, *args, **kwargs):
        profileuser = checkprofile(request)
        posts = Posts.objects.filter(author = profileuser).order_by('-timestamp')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/posts/postlike/<post_id>/

    @action(detail=False, methods=['PUT'], url_path="postlike/(?P<pk>[^/.]+)")
    def postlike(self, request, pk=None, action=None, *args, **kwargs):
        profileuser = checkprofile(request)
        post = get_object_or_404(Posts, pk=pk)
        try:
            if request.data['action'] == 'like':
                like = Postlike(user=profileuser, post=post).save()
                serializer = PostSerializer(post, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "%s" % (e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if request.data['action'] == 'unlike':
            Postlike.objects.filter(user=profileuser, post=post).delete()
            serializer = PostSerializer(post, many=False)
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response({"message": "Serialization Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(detail=False, methods=['GET'], url_path="postcheck/(?P<pk>[^/.]+)")
    def postcheck(self, request, pk=None, *args, **kwargs):
        user = checkprofile(request)
        post = get_object_or_404(Posts, pk=pk)
        result = Postlike.objects.filter(user=user, post=post).count() > 0
        return Response({"result": result}, status=status.HTTP_200_OK)


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

# http://127.0.0.1:8000/api/comments/newcomment/<post_id>/

    @action(detail=False, methods=['POST'], url_path="newcomment/(?P<pk>[^/.]+)")
    def newComment(self, request, pk=None, *args, **kwargs):
        profileuser = checkprofile(request)
        post = get_object_or_404(Posts, pk=pk)
        if 'body' in request.data:
            if 'thumbnail' in request.data:
                comment = Comments.objects.create(body=profanity.censor(
                    request.data['body']), thumbnail=request.data['thumbnail'], posts=post, author=profileuser)
            if not 'thumbnail' in request.data:
                comment = Comments.objects.create(body=profanity.censor(
                    request.data['body']), posts=post, author=profileuser)
            comments = Comments.objects.filter(posts = post).order_by('-timestamp')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Serialization Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)

# http://127.0.0.1:8000/api/comments/<comment_id>/

    def destroy(self, request, pk=None, *args, **kwargs):
        Comments.objects.get(id=pk).delete()
        comments = Comments.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/comments/<comment_id>/

    def update(self, request, pk=None, body=None, thumbnail=None, *args, **kwargs):
        comment = get_object_or_404(Comments, pk=pk)
        if 'body' in request.data:
            comment.body = profanity.censor(request.data['body'])
        if 'thumbnail' in request.data:
            comment.thumbnail = request.data['thumbnail']
        comment.save()
        comments = Comments.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/comments/getcomments/<post_id>/

    @action(detail=False, url_path="getcomments/(?P<pk>[^/.]+)")
    def getComment(self, request, pk=None, *args, **kwargs):
        post = get_object_or_404(Posts, pk=pk)
        comments = Comments.objects.filter(posts=post).order_by('-timestamp')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# http://127.0.0.1:8000/api/comments/commentlike/<comment_id>/

    @action(detail=False, methods=['PUT'], url_path="commentlike/(?P<pk>[^/.]+)")
    def commentlike(self, request, pk=None, action=None, *args, **kwargs):
        profileuser = checkprofile(request)
        comment = get_object_or_404(Comments, pk=pk)
        comments = Comments.objects.all().order_by('-id')
        try:
            if request.data['action'] == 'like':
                like = Commentlike(user=profileuser, comment=comment).save()
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "%s" % (e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if request.data['action'] == 'unlike':
            Commentlike.objects.filter(user=profileuser, comment=comment).delete()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PollViewset(viewsets.ModelViewSet):

    queryset = Polls.objects.all()
    serializer_class = PollSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        user = checkprofile(request)
        try:
            question = profanity.censor(request.data['question'])
            choice1 = profanity.censor(request.data['choice1'])
            choice2 = profanity.censor(request.data['choice2'])
            choice3 = profanity.censor(request.data['choice3'])
            choice4 = profanity.censor(request.data['choice4'])
            choice5 = profanity.censor(request.data['choice5'])
            newpoll = Polls.objects.create(question=question, choice1=choice1, choice2=choice2,
                                           choice3=choice3, choice4=choice4, choice5=choice5, author=user)
            print(5)
            serializer = PollSerializer(newpoll, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            try:
                question = profanity.censor(request.data['question'])
                choice1 = profanity.censor(request.data['choice1'])
                choice2 = profanity.censor(request.data['choice2'])
                choice3 = profanity.censor(request.data['choice3'])
                choice4 = profanity.censor(request.data['choice4'])
                newpoll = Polls.objects.create(
                    question=question, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, author=user)
                print(4)
                serializer = PollSerializer(newpoll, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                try:
                    question = profanity.censor(request.data['question'])
                    choice1 = profanity.censor(request.data['choice1'])
                    choice2 = profanity.censor(request.data['choice2'])
                    choice3 = profanity.censor(request.data['choice3'])
                    newpoll = Polls.objects.create(
                        question=question, choice1=choice1, choice2=choice2, choice3=choice3, author=user)
                    print(3)
                    serializer = PollSerializer(newpoll, many=False)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                    question = profanity.censor(request.data['question'])
                    choice1 = profanity.censor(request.data['choice1'])
                    choice2 = profanity.censor(request.data['choice2'])
                    newpoll = Polls.objects.create(
                        question=question, choice1=choice1, choice2=choice2, author=user)
                    print(2)
                    serializer = PollSerializer(newpoll, many=False)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Serialization Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, pk=None, *args, **kwargs):
        poll = get_object_or_404(Polls, pk=pk)
        try:
            poll.question = profanity.censor(request.data['question'])
            poll.choice1 = profanity.censor(request.data['choice1'])
            poll.choice2 = profanity.censor(request.data['choice2'])
            poll.choice3 = profanity.censor(request.data['choice3'])
            poll.choice4 = profanity.censor(request.data['choice4'])
            poll.choice5 = profanity.censor(request.data['choice5'])
            poll.save()
            print(5)
            polls = Polls.objects.all()
            serializer = PollSerializer(polls, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            try:
                poll.question = profanity.censor(request.data['question'])
                poll.choice1 = profanity.censor(request.data['choice1'])
                poll.choice2 = profanity.censor(request.data['choice2'])
                poll.choice3 = profanity.censor(request.data['choice3'])
                poll.choice4 = profanity.censor(request.data['choice4'])
                poll.save()
                print(4)
                polls = Polls.objects.all()
                serializer = PollSerializer(polls, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                try:
                    poll.question = profanity.censor(request.data['question'])
                    poll.choice1 = profanity.censor(request.data['choice1'])
                    poll.choice2 = profanity.censor(request.data['choice2'])
                    poll.choice3 = profanity.censor(request.data['choice3'])
                    poll.save()
                    print(3)
                    polls = Polls.objects.all()
                    serializer = PollSerializer(polls, many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                    poll.question = profanity.censor(request.data['question'])
                    poll.choice1 = profanity.censor(request.data['choice1'])
                    poll.choice2 = profanity.censor(request.data['choice2'])
                    poll.save()
                    print(2)
                    polls = Polls.objects.all()
                    serializer = PollSerializer(polls, many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Serialization Error"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def list(self, request, *args, **kwargs):
        polls = Polls.objects.all().order_by('-timestamp')
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path="latestpoll")
    def latestpoll(self, request, *args, **kwargs):
        poll = Polls.objects.all().order_by('-timestamp')[0]
        serializer = PollSerializer(poll, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path="mypolls")
    def userPolls(self, request, *args, **kwargs):
        profileuser = checkprofile(request)
        polls = get_list_or_404(Polls, author=profileuser)
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PUT'], url_path="pollvote/(?P<pk>[^/.]+)")
    def pollvote(self, request, pk=None, choice=None, *args, **kwargs):
        user = checkprofile(request)
        poll = get_object_or_404(Polls, pk=pk)
        selected = request.data['choice']
        try:
            if poll.completed == False:
                if selected == poll.choice1:
                    voting = PollVote(user=user, poll=poll).save()
                    poll.choice1_total += 1
                elif selected == poll.choice2:
                    voting = PollVote(user=user, poll=poll).save()
                    poll.choice2_total += 1
                elif selected == poll.choice3:
                    voting = PollVote(user=user, poll=poll).save()
                    poll.choice3_total += 1
                elif selected == poll.choice4:
                    voting = PollVote(user=user, poll=poll).save()
                    poll.choice4_total += 1
                elif selected == poll.choice5:
                    voting = PollVote(user=user, poll=poll).save()
                    poll.choice5_total += 1
                poll.save()
                return Response({"message": "Poll voted"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "Poll Timed out"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"message": "%s" % (e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
