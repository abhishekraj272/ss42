from .serializers import Spost,Smessage, PostSerializer, CommentSerializer,ImgSerializer
from .serializers import PostSerializer_read, ImgSerializer_read, MsgSerializer_read
from posts.models import Post,Message, Comment,Img
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
# from rest_framework.Status import status
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404,ListAPIView
from posts.api import serializers
from rest_framework.exceptions import ValidationError
from posts.api.serializers import Spost
from posts.models import Post
from posts.api.permissions import IsAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from django.contrib.auth.models import User
from developer.models import Developers
from posts.models import Post

from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db import close_old_connections
from rest_framework import filters
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse, JsonResponse
from objects.models import Profile

from rest_framework_api_key.permissions import HasAPIKey  # Permission for API Key check
from django.views.decorators.csrf import csrf_exempt

# from rest_framework.responseim
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     # lookup_field="id"
#     serializer_class=Suser
@csrf_exempt
def vote_post(request, pid, uid, query):
    if query == 'upvote':
        post = Post.objects.get(id=pid)

        usr = User.objects.get(id=uid)

        if usr in post.genuine.all():
            return JsonResponse({'message': "Post already upvoted !"})

        post.genuine.add(usr)

        if usr in post.spam.all():
            post.spam.remove(usr)

        post.save()

        try:
            obj = Profile.objects.get(username=post.author.username)
            val = obj.Scrapcoins
            obj.Scrapcoins = val + 1
            obj.save()
        except:
            obj = Profile.objects.create(
                username=post.author.username,
                userid = post.author.id,
                tags = [""],
                Scrapcoins = 1
                )

        scrapcoins = len(post.genuine.values()) - len(post.spam.values())
        if scrapcoins < 0:
            scrapcoins = 0
        payload = {
            'post_id': post.id,
            'upvotes': len(post.genuine.values()),
            'downvotes': len(post.spam.values()),
            'scrapcoins': scrapcoins
        }

        return JsonResponse(payload)

    elif query == 'downvote':
        post = Post.objects.get(id=pid)

        usr = User.objects.get(id=uid)

        if usr in post.spam.all():
            return JsonResponse({'message': "Post already downvoted !"})

        post.spam.add(usr)

        if usr in post.genuine.all():
            post.genuine.remove(usr)

        post.save()

        try:
            obj = Profile.objects.get(username=post.author.username)
            val = obj.Scrapcoins
            obj.Scrapcoins = val - 1
            obj.save()
        except:
            return HttpResponse(status=404)

        scrapcoins = len(post.genuine.values()) - len(post.spam.values())
        if scrapcoins < 0:
            scrapcoins = 0
        payload = {
            'post_id': post.id,
            'upvotes': len(post.genuine.values()),
            'downvotes': len(post.spam.values()),
            'scrapcoins': scrapcoins
        }

        return JsonResponse(payload)
@csrf_exempt
def vote_img(request, pid, uid, query):
    if query == 'upvote':
        img = Img.objects.get(id=pid)

        usr = User.objects.get(id=uid)

        if usr in img.genuine.all():
            return JsonResponse({'message': "Image already upvoted !"})

        img.genuine.add(usr)

        if usr in img.spam.all():
            img.spam.remove(usr)

        img.save()

        try:
            obj = Profile.objects.get(username=img.author.username)
            val = obj.Scrapcoins
            obj.Scrapcoins = val + 1
            obj.save()
        except:
            obj = Profile.objects.create(
                username=img.author.username,
                userid = img.author.id,
                tags = [""],
                Scrapcoins = 1
                )

        scrapcoins = len(img.genuine.values()) - len(img.spam.values())
        if scrapcoins < 0:
            scrapcoins = 0
        payload = {
            'image_id': img.id,
            'upvotes': len(img.genuine.values()),
            'downvotes': len(img.spam.values()),
            'scrapcoins': scrapcoins
        }

        return JsonResponse(payload)

    elif query == 'downvote':
        img = Img.objects.get(id=pid)

        usr = User.objects.get(id=uid)

        if usr in img.spam.all():
            return JsonResponse({'message': "Image already downvoted !"})

        img.spam.add(usr)

        if usr in img.genuine.all():
            img.genuine.remove(usr)

        img.save()

        try:
            obj = Profile.objects.get(username=img.author.username)
            val = obj.Scrapcoins
            obj.Scrapcoins = val - 1
            obj.save()
        except:
            return HttpResponse(status=404)

        scrapcoins = len(img.genuine.values()) - len(img.spam.values())
        if scrapcoins < 0:
            scrapcoins = 0
        payload = {
            'image_id': img.id,
            'upvotes': len(img.genuine.values()),
            'downvotes': len(img.spam.values()),
            'scrapcoins': scrapcoins
        }

        return JsonResponse(payload)
@csrf_exempt
def vote_msg(request, pid, uid, query):
    if query == 'upvote':
        msg = Message.objects.get(id=pid)

        usr = User.objects.get(id=uid)

        if usr in msg.genuine.all():
            return JsonResponse({'message': "Message already upvoted !"})

        msg.genuine.add(usr)

        if usr in msg.spam.all():
            msg.spam.remove(usr)

        msg.save()

        try:
            obj = Profile.objects.get(username=msg.author.username)
            val = obj.Scrapcoins
            obj.Scrapcoins = val + 1
            obj.save()
        except:
            obj = Profile.objects.create(
                username=msg.author.username,
                userid = msg.author.id,
                tags = [""],
                Scrapcoins = 1
                )

        scrapcoins = len(msg.genuine.values()) - len(msg.spam.values())
        if scrapcoins < 0:
            scrapcoins = 0
        payload = {
            'message_id': msg.id,
            'upvotes': len(msg.genuine.values()),
            'downvotes': len(msg.spam.values()),
            'scrapcoins': scrapcoins
        }

        return JsonResponse(payload)

    elif query == 'downvote':
        msg = Message.objects.get(id=pid)


        usr = User.objects.get(id=uid)

        if usr in msg.spam.all():
            return JsonResponse({'message': "Message already downvoted !"})

        msg.spam.add(usr)

        if usr in msg.genuine.all():
            msg.genuine.remove(usr)

        msg.save()

        try:
            obj = Profile.objects.get(username=msg.author.username)
            val = obj.Scrapcoins
            obj.Scrapcoins = val - 1
            obj.save()
        except:
            return HttpResponse(status=404)

        scrapcoins = len(msg.genuine.values()) - len(msg.spam.values())
        if scrapcoins < 0:
            scrapcoins = 0
        payload = {
            'message_id': msg.id,
            'upvotes': len(msg.genuine.values()),
            'downvotes': len(msg.spam.values()),
            'scrapcoins': scrapcoins
        }

        return JsonResponse(payload)

class SortedPostViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Post.objects.all()
        tags = []
        tag1 = self.request.query_params.get('tag1', '')
        tags.append(tag1)
        tag2 = self.request.query_params.get('tag2', '')
        tags.append(tag2)
        tag3 = self.request.query_params.get('tag3', '')
        tags.append(tag3)
        tag4 = self.request.query_params.get('tag4', '')
        tags.append(tag4)
        tag5 = self.request.query_params.get('tag5', '')
        tags.append(tag5)
        tag6 = self.request.query_params.get('tag6', '')
        tags.append(tag6)
        tag7 = self.request.query_params.get('tag7', '')
        tags.append(tag7)
        tag8 = self.request.query_params.get('tag8', '')
        tags.append(tag8)
        tag9 = self.request.query_params.get('tag9', '')
        tags.append(tag9)
        tag10 = self.request.query_params.get('tag10', '')
        tags.append(tag10)
        # print(tags)
        # print(self.request.stream)

        filtered_ids = []
        for tag in tags:
            if tag:

                for post in queryset:
                    req_tag = post.tags.filter(name=tag)
                    # print(req_tag)
                    if req_tag.exists():
                        filtered_ids.append(post.id)
        return queryset.filter(id__in=filtered_ids)

    serializer_class=Spost
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)
class SortedMessageViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Message.objects.all()
        tags = []
        tag1 = self.request.query_params.get('tag1', '')
        tags.append(tag1)
        tag2 = self.request.query_params.get('tag2', '')
        tags.append(tag2)
        tag3 = self.request.query_params.get('tag3', '')
        tags.append(tag3)
        tag4 = self.request.query_params.get('tag4', '')
        tags.append(tag4)
        tag5 = self.request.query_params.get('tag5', '')
        tags.append(tag5)
        tag6 = self.request.query_params.get('tag6', '')
        tags.append(tag6)
        tag7 = self.request.query_params.get('tag7', '')
        tags.append(tag7)
        tag8 = self.request.query_params.get('tag8', '')
        tags.append(tag8)
        tag9 = self.request.query_params.get('tag9', '')
        tags.append(tag9)
        tag10 = self.request.query_params.get('tag10', '')
        tags.append(tag10)
        # print(tags)
        # print(self.request.stream)

        filtered_ids = []
        for tag in tags:
            if tag:

                for message in queryset:
                    req_tag = message.tags.filter(name=tag)
                    # print(req_tag)
                    if req_tag.exists():
                        filtered_ids.append(message.id)
        return queryset.filter(id__in=filtered_ids)

    serializer_class=Smessage
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)

class SortedImageViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Img.objects.all()
        tags = []
        tag1 = self.request.query_params.get('tag1', '')
        tags.append(tag1)
        tag2 = self.request.query_params.get('tag2', '')
        tags.append(tag2)
        tag3 = self.request.query_params.get('tag3', '')
        tags.append(tag3)
        tag4 = self.request.query_params.get('tag4', '')
        tags.append(tag4)
        tag5 = self.request.query_params.get('tag5', '')
        tags.append(tag5)
        tag6 = self.request.query_params.get('tag6', '')
        tags.append(tag6)
        tag7 = self.request.query_params.get('tag7', '')
        tags.append(tag7)
        tag8 = self.request.query_params.get('tag8', '')
        tags.append(tag8)
        tag9 = self.request.query_params.get('tag9', '')
        tags.append(tag9)
        tag10 = self.request.query_params.get('tag10', '')
        tags.append(tag10)
        # print(tags)
        # print(self.request.stream)

        filtered_ids = []
        for tag in tags:
            if tag:

                for img in queryset:
                    req_tag = img.tags.filter(name=tag)
                    # print(req_tag)
                    if req_tag.exists():
                        filtered_ids.append(img.id)
        return queryset.filter(id__in=filtered_ids)

    serializer_class=ImgSerializer
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        post = Post.objects.get(id=post_id)
        content = self.request.data.get('content')

        serializer.save(
            author = self.request.user,
            post = Post.objects.get(id=post_id)
        )
        comment = Comment.objects.filter(content=content)[0]
        post.comments.add(comment)
        post.save()

class ForServicePostViewSet(viewsets.ModelViewSet):
    close_old_connections()
    queryset = Post.objects.all()

    search_fields = ['url']

    # search_fields = ('url','tags','review')
    serializer_class = PostSerializer_read
    http_method_names = ['get']
    filter_backends = (filters.SearchFilter,)
    permission_classes =[IsAuthorOrReadOnly,IsAuthenticatedOrReadOnly]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)
    close_old_connections()


class PostViewSet(viewsets.ModelViewSet):
    close_old_connections()
    queryset = Post.objects.all()
    search_fields = ['url']
    filter_backends = (filters.SearchFilter,)
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer_read
        else:
            return PostSerializer

    def create(self, request):
        url = request.data.get('url')
        author = str(request.user)
        filtered_url = Post.objects.filter(url=url)
        already_exists = False
        for each_url in filtered_url:
            if each_url.author.username == author:
                already_exists = True
        if already_exists:
            return Response({"details" : "Review already exists ! "}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super(PostViewSet, self).create(request)

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
    close_old_connections()
class FakePostViewSet(viewsets.ModelViewSet):
    close_old_connections()
    # lookup_field="id"
    search_fields = ['url']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer_read
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)

    def get_queryset(self):
        return  Post.objects.filter(fake=True)

    close_old_connections()


class ForServiceImgViewSet(viewsets.ModelViewSet):
    close_old_connections()
    parser_class = (FileUploadParser,)
    queryset = Img.objects.all()
    serializer_class = ImgSerializer_read
    http_method_names = ['get']
    permission_classes =[HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)
    close_old_connections()
class ImgViewSet(viewsets.ModelViewSet):
    parser_class = (FileUploadParser,)
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)
    queryset = Img.objects.all()

    def get_serializer_class(self):
        # print(self.request.method)
        if self.request.method == 'GET':
            return ImgSerializer_read
        else:
            return ImgSerializer

    def perform_create(self, serializer):
        serializer.save(author=serializer.context['request'].user)
class FakeImgViewSet(viewsets.ModelViewSet):
    close_old_connections()
    # lookup_field="id"
    search_fields = ['url']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ImgSerializer_read
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)

    def get_queryset(self):
        return  Img.objects.filter(fake=True)

    close_old_connections()

class ForServiceMsgViewSet(viewsets.ModelViewSet):
    close_old_connections()
    search_fields = ['url']
    queryset = Img.objects.all()
    serializer_class = MsgSerializer_read
    http_method_names = ['get']
    filter_backends = (filters.SearchFilter,)
    permission_classes =[HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)
    close_old_connections()

class FakeMsgViewSet(viewsets.ModelViewSet):
    close_old_connections()
    # lookup_field="id"
    search_fields = ['url']
    filter_backends = (filters.SearchFilter,)
    serializer_class = MsgSerializer_read
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)

    def get_queryset(self):
        return  Message.objects.filter(fake=True)

    close_old_connections()
class MsgViewSet(viewsets.ModelViewSet):
    close_old_connections()
    # parser_class = (FileUploadParser,)

    queryset = Message.objects.all()

    def get_serializer_class(self):
        # print(self.request.method)
        if self.request.method == 'GET':
            return MsgSerializer_read
        else:
            return Smessage
    # lookup_field="id"
    # search_fields = ['url']
    # filter_backends = (filters.SearchFilter,)


    serializer_class=Smessage
    permission_classes =[IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly, HasAPIKey]
    authentication_classes =(TokenAuthentication,JSONWebTokenAuthentication)
    # def create(self, request):
    #     url = request.data.get('url')
    #     author = str(request.user)
    #     filtered_url = Post.objects.filter(url=url)
    #     already_exists = False
    #     for each_url in filtered_url:
    #         if each_url.author.username == author:
    #             already_exists = True
    #     if already_exists:
    #         return Response({"details" : "Review already exists ! "}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return super(PostViewSet, self).create(request)
    def perform_create(self,serializer):

        serializer.save(author=self.request.user)
    close_old_connections()
    # @action(detail=True,methods=['POST'])
    # def rate_post(self,request,pk=None):
    #     if 'stars' in request.data:
    #         post=Post.objects.get(id=pk)
    #         stars = request.data['stars']
    #         user=request.user
    #         # user = User.objects.get(id=1)
    #         print('hser title' ,user.username)
    #         response={'message':'ok this is working'}
            # try:
            #     rating=Rating.objects.get(user=user.id, Post=post.id)
            #     rating.stars=stars
            #     rating.save()
            #     serializer=Srating(rating,many=False)
            #     response={'message':'rating updated','result':serializer.data}
            #     return Response(response,status=status.HTTP_200_OK)
            # except:
            #     rating = Rating.objects.create(user=user,Post=post,stars=stars)
            #     serializer=Srating(rating,many=False)
            #     response={'message':'rating created','result':serializer.data}
            #     return Response(response,status=status.HTTP_200_OK)

            # return Response(response,status=status.HTTP_200_OK)
        # else:
        #     response={'message':'no stars'}
        #     return Response(response,status=status.HTTP_200_OK)

# class CommentsCreateAPIView(generics.CreateAPIView):
#     queryset=comments.objects.all()
#     serializer_class=Scomments
#     permission_classes=[IsAuthorOrReadOnly]
#     def perform_create(self,serializer):
#         request_user= self.request.user
#         kwarg_id=self.kwargs.get("id")
#         post=get_object_or_404(comments,id=kwarg_id)
#         serializer.save(author=request.user,post=post)
# class RatingViewSet(viewsets.ModelViewSet):
#     queryset=Rating.objects.all()
#     serializer_class=Srating
#     authentication_classes =(TokenAuthentication,)

# class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=Spost
    permission_classes=[IsAuthorOrReadOnly,IsAuthenticatedOrReadOnly, HasAPIKey]
class PostLikeView(APIView):
    serializer_class=Spost
    permission_classes=[IsAuthenticatedOrReadOnly, HasAPIKey]
    def delete(self,request,pk):
        post=get_object_or_404(Post,pk=pk)
        user=request.user
        post.voters.remove(user)
        serializer_context={"request":request}
        serializer=self.serializer_class(post,context=serializer_context)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,pk):
        post=get_object_or_404(Post,pk=pk)
        user=request.user
        post.voters.add(user)
        serializer_context={"request":request}
        serializer=self.serializer_class(post,context=serializer_context)
        return Response(serializer.data,status=status.HTTP_200_OK)
class userView(mixins.RetrieveModelMixin,ListAPIView):
    """ this is to get the  all the objects created by a  indiviual user through id"""
    serializer_class=serializers.UserDetailSerializer
    # permission_classes=[IsOwnerOrReadOnly,permissions.IsAuthenticatedOrReadOnly]
    lookup_field='id'
    def get_queryset(self):
        if self.kwargs['id']:
            return Post.objects.all().filter(user=self.kwargs['id'])
###########
# class Postsnippet(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,Spost
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     serializer_class = Spost
#     lookup_field='id'
#     def get_queryset(self):
#         request = self.request
#         print(request.user)
#         qs = Post.objects.all()
#         query = request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#         return qs
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
# class Postsnippet(viewsets.ModelViewSet):
#     serializer_class=Spost
#     queryset= Post.objects.all()
@csrf_exempt
@api_view(["GET","POST"])
def api_get_create(request):


    if request.method == "GET":
        post=Post.objects.all()
        serializer= Spost(post,many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer= Spost(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@csrf_exempt
@api_view(["GET","PUT","DELETE"])
def api_delete(request,pk):
    # post=Post.objects.filter(pk=pk)
    try:
        post = Post.objects.get(pk=pk)  # Lookup a specific object
    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer= Spost(post,many=True)

        return Response(serializer.data)
    elif request.method == "PUT":
        # post=Post.objects.filter(pk=pk)
        serializer= Spost(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print("noot correct")
        return Response(serializer.data)
