from rest_framework import serializers
from posts.models import Post,Message,Comment,Img,PostAdvertisment
from django.contrib.auth.models import User
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from django.http import HttpResponse
#########
# class Suser(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=('id','username','password')
#         extra_kwargs={'password':{'write_only':True,'required':True}}
#     def create(self,validated_data):
#         user=User.objects.create(**validated_data)
#         return user
#
# class Scomments(serializers.ModelSerializer):
#     comments_count=serializers.SerializerMethodField(read_only=True)
#     user_has_commented=serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model=comments
#         fields = '__all__'
#     def get_comments_count(self,instance):
#         return instance.comments.count()
#     def get_user_has_voted(self,instance):
#         request=self.context.get("request")
#         return instance.commentss.filter(pk=request.user.pk).exists()
class UserDetailSerializer(serializers.ModelSerializer):
    """for all  getting all objectws of a particular user """
    class Meta:
        model=Post
        fields=['id',
                'author',
                'review',
                ]

class ImgSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    author = serializers.StringRelatedField()
    # post   = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Img
        fields='__all__'

class ImgSerializer_read(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    author = serializers.SerializerMethodField(method_name='get_user_type')
    # post   = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Img
        # fields='__all__'
        fields = ('id', 'author','picture', 'created_at', 'tags', 'fake')
    def get_user_type(self, instance):
        if instance.anonymous:
            return "anonymous"
        else:
            return instance.author.username

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post   = serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Comment
        fields='__all__'
class PostAdvertisementSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)
    # post   = serializers.StringRelatedField(read_only=True)

    class Meta:
        model=PostAdvertisment
        fields='__all__'

class StringListField(serializers.ListField): # get from http://www.django-rest-framework.org/api-guide/fields/#listfield
    child = serializers.CharField()

    def to_representation(self, data):
        return ' '.join(data.values_list('name', flat=True))
class PostSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = StringListField()
   
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, required=False, read_only=True)
    advertisement = PostAdvertisementSerializer()

    # advertisement = serializers.SlugRelatedField(
    #     queryset=PostAdvertisment.objects.all(),   
    #     slug_field='advertisement'
    #      )
    # category_name = serializers.CharField(source='advertisement.title')
    class Meta:
        model = Post
        fields = ('id','title','rate','author','content','review','url','tags', 'fake','comments', 'created_at', 'anonymous','advertisement')
    # def create(self, validated_data):
    #     tag = validated_data.pop('advertisement')
    #     tag_instance, created =PostAdvertisment.objects.get_or_create(title=tag)
    #     article_instance = Post.objects.create(**validated_data, advertisement=tag_instance)
    #     return article_instance 
    # def create(self, validated_data):
    #     serializer = self.get_serializer(data=self.request.data)
    #     advertisment =  self.request.data.pop('advertisement')
    #     company_instance = PostAdvertisment.objects.filter(id=advertisment).first()
    #     if not serializer.is_valid():
    #         print(serializer.errors)
    #     data = serializer.validated_data
    #     serializer.save(PostAdvertisment=company_instance)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 
    def create(self,validated_data):
        validated_data["advertisement"] = PostAdvertisment.objects.create(**validated_data["advertisement"])
        tags = validated_data.pop('tags')
        instance = super(PostSerializer, self).create(validated_data)
        instance.tags.set(*tags)
        return instance
        post = Post.objects.create(**validated_data)
        return post
    def update(self, instance, validated_data):
    
        # Update the  instance
        instance.review = validated_data['review']
        instance.save()

        return instance

        # advertisement=validated_data.pop('advertisement')
        # post = Post.objects.create(**validated_data)
        # post.advertisement = PostAdvertisment.objects.create(**advertisement)
        # post.save()
        # return post        



        # advertisement=validated_data.pop('advertisement')
      

        # post=Post.objects.create(**validated_data)
        # # for advertise in advertisement:
        # postad=PostAdvertisment.objects.create(**advertisement, post=post)

        # return post  
    def get_likes_count(self,instance):
        return instance.voters.count()
    def get_user_has_voted(self,instance):
        request=self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

class PostSerializer_read(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(required=False,read_only=True)
    author = serializers.SerializerMethodField(method_name='get_user_type')
    comments = CommentSerializer(many=True, required=False)
    # advertisement=serializers.ReadOnlyField(read_only=True)

    # advertisement = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    advertisement = PostAdvertisementSerializer()
    # category_name = serializers.CharField(source='advertisement')
    # category_url=serializers.URLField(source='advertisement.url')


    class Meta:
        model = Post
        fields = ('id','title','rate','author','content','review','url','fake','tags','comments', 'created_at','advertisement')
    def get_user_type(self, instance):
        if instance.anonymous:
            return "anonymous"
        else:
            return instance.author.username
    def get_likes_count(self,instance):
        return instance.voters.count()
    def get_user_has_voted(self,instance):
        request=self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

class Spost(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()

    author=serializers.StringRelatedField(read_only=True)
    # comments= CommentSerializer(read_only=True)
    # likes_count=serializers.SerializerMethodField(read_only=True)
    # user_has_voted=serializers.SerializerMethodField(read_only=True)
    ## for string related field without displaying it as numerics , it displays the direct object of that object"
    # user=Scomments()
    class Meta:
        model = Post
        fields = ('id','title','rate','author','content','review','url','tags','comments')
    def get_likes_count(self,instance):
        return instance.voters.count()
    def get_user_has_voted(self,instance):
        request=self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

class Smessage(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    author=serializers.StringRelatedField(read_only=True)
    # likes_count=serializers.SerializerMethodField(read_only=True)
    # user_has_voted=serializers.SerializerMethodField(read_only=True)
    ## for string related field without displaying it as numerics , it displays the direct object of that object"
    # user=Scomments()
    class Meta:
        model = Message
        fields = ('id','title','rate','author','content','review', 'created_at', 'tags', 'fake', 'anonymous')
    def get_likes_count(self,instance):
        return instance.voters.count()
    def get_user_has_voted(self,instance):
        request=self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

class MsgSerializer_read(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField(required=False)
    author = serializers.SerializerMethodField(method_name='get_user_type')
    # likes_count=serializers.SerializerMethodField(read_only=True)
    # user_has_voted=serializers.SerializerMethodField(read_only=True)
    ## for string related field without displaying it as numerics , it displays the direct object of that object"
    # user=Scomments()
    class Meta:
        model = Message
        fields = ('id','title','rate','author','content','review', 'created_at', 'tags', 'fake')

    def get_user_type(self, instance):
        if instance.anonymous:
            return "anonymous"
        else:
            return instance.author.username

    def get_likes_count(self,instance):
        return instance.voters.count()
    def get_user_has_voted(self,instance):
        request=self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()
# class Srating(serializers.ModelSerializer):
#     class Meta:
#         model=Rating
#         fields='__all__'
