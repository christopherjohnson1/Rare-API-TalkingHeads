from django.urls import path
from rest_framework import routers

from rareserverapi.views import Categories, Posts, register_user, login_user, Tags, PostTags, Profiles, Subscriptions, Users, Reactions, PostReactions
from rareserverapi.views import Comments
from django.conf.urls import include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', Categories, 'category')
router.register(r'comments', Comments, 'comment')
router.register(r'posts', Posts, 'post')
router.register(r'tags', Tags, 'tag')
router.register(r'posttags', PostTags, 'posttag')
router.register(r'profile', Profiles, 'profile')
router.register(r'subscriptions', Subscriptions, 'subscription')
router.register(r'users', Users, 'user')
router.register(r'postreactions', PostReactions, 'postreaction')
router.register(r'reactions', Reactions, 'reaction')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
