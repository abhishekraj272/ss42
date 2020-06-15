# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('', admin.site.urls),
# ]
from django.urls import include, path
from rest_framework import routers
from posts.api import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter,DefaultRouter

from posts.models import Post, Comment, Message, Img

from django.conf import settings
from posts.api  import views
from django.conf.urls.static import static

router = DefaultRouter()


router.register(r'post', views.PostViewSet)
router.register(r'post/<int:pk>/',views.PostViewSet)
router.register(r'msg', views.MsgViewSet)
router.register(r'img', views.ImgViewSet)

router.register(r'service/post', views.ForServicePostViewSet)
router.register(r'service/msg', views.ForServiceMsgViewSet)
router.register(r'service/img', views.ForServiceImgViewSet)

router.register(r'fake_post', views.FakePostViewSet, Post)
router.register(r'fake_msg', views.FakeMsgViewSet, Message)
router.register(r'fake_img', views.FakeImgViewSet, Img)

router.register(r'comments', views.CommentViewSet, Comment)
router.register(r'ptags', views.SortedPostViewSet, Post)
router.register(r'mtags', views.SortedMessageViewSet, Message)
router.register(r'itags', views.SortedImageViewSet, Img)
# router.register(r'ratings', views.RatingViewSet)
# router.register(r'users', views.UserViewSet)


# router.register(r'users', views.UserViewSet)
# router = routers.DefaultRouter()
# router.register('list', views.Postsnippet)
# router.register()
# The API URLs are now determined automatically by the router.
urlpatterns = [
    # path('list/(?P<id>[0-9]+)/$', views.Postsnippet.as_view(),name='post_list'),
    path('',  include(router.urls)),
    # path('post/<slug:id>/comment',views.CommentsCreateAPIView.as_view(),name="comment"),
    path('post/<slug:id>/detail',views.PostRUDView.as_view(),name="detail"),
    path('post/<int:pk>/like',views.PostLikeView.as_view(),name="like"),
    path('post/vote/<int:pid>/<int:uid>/<str:query>', views.vote_post),
    path('img/vote/<int:pid>/<int:uid>/<str:query>', views.vote_img),
    path('msg/vote/<int:pid>/<int:uid>/<str:query>', views.vote_msg),
    # url(r'^nice/(?P<id>\d+)$',userView.as_view(),name='username'),


    # path('get',views.api_get_create,name='get_test'),
    # path('update/<int:pk>/',views.api_delete,name='put_test')

]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
