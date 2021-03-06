from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User
from rareserverapi.models import Comment, Post
from rareserverapi.models import  RareUser

class CommenterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'id')

class RareUserSerializer(serializers.ModelSerializer):

    user = CommenterUserSerializer(many=False)
    class Meta:

        model = RareUser
        fields = ( 'profile_image_url', 'user', 'id')

class CommentSerializer(serializers.ModelSerializer):

    commenter = RareUserSerializer(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'commenter_id', 'content', 'subject', 'commenter', 'is_owner', 'created_on')
        depth = 1


class Comments(ViewSet):
    """comments for rare"""
    def create(self, request):
        """post operations for adding comments"""

        commenter = RareUser.objects.get(user=request.auth.user)
        
        comment = Comment()

        comment.content = request.data['content']
        comment.subject = request.data['subject']
        comment.created_on = ""

        post = Post.objects.get(pk=request.data["post_id"])
        
        comment.commenter = commenter

        comment.post = post

        try:
            comment.save()

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
        """single comment"""
        try:
            comment = Comment.objects.get(pk=pk)

            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    
    def list(self, request):
        """all comments"""
        comments = Comment.objects.all() # all comments commenter_id 

        current_user = RareUser.objects.get(user=request.auth.user) #commenter is id of currently logged in user

        #filters comments by post_id  -- comments?post_id=1
        post = self.request.query_params.get('post_id', None)
        if post is not None:
            comments = comments.filter(post_id=post)

            for comment in comments:
                comment.is_owner = False
                if comment.commenter_id == current_user.id:
                    comment.is_owner = True
                

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
        


        

    def update(self, request, pk=None):
        """edits comment"""

        commenter = RareUser.objects.get(user=request.auth.user)

        comment = Comment.objects.get(pk=pk)

        comment.content = request.data['content']
        comment.subject = request.data['subject']
        comment.created_on = request.data['created_on']

        post = Post.objects.get(pk=request.data["post_id"])
        
        comment.commenter = commenter

        comment.post = post

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    
    def destroy(self, request, pk=None):
        """deletes comment"""

        try:
            comment = Comment.objects.get(pk=pk)

            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    


    