from django.db.models import Q
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny , IsAdminUser
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_429_TOO_MANY_REQUESTS
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import FriendShipRequest
from .enums import RequestStatusEnum
from .serializers import FriendShipRequestSerializer
from UserAuthentication.serializers import UserSerializer
from UserAuthentication.models import User
from datetime import datetime , timedelta

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    

    def post(self, request):
        try:
            to_user_id = request.data.get('to_user')
            to_user = User.objects.get(id=to_user_id)
            from_user = request.user

            one_minute_ago = timezone.now() - timedelta(minutes=1)
            recent_requests = FriendShipRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
            if recent_requests >= 3:
                return Response({'error': 'You cannot send more than 3 friend requests in a minute'}, status=HTTP_429_TOO_MANY_REQUESTS)

            friend_request, created = FriendShipRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
            if not created:
                return Response({'error': 'Friend request already sent'}, status=HTTP_400_BAD_REQUEST)
            
            serialized_friend_request = FriendShipRequestSerializer(friend_request)

            return Response({'message': 'Friend request sent successfully', 'request': serialized_friend_request.data}, status=HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)    

class FriendRequestResponseView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, request_id, action):
        try:
            friend_request = FriendShipRequest.objects.get(id=request_id, to_user=request.user)

            if action == 'accept':
                friend_request.status = RequestStatusEnum.Accepted.value
            elif action == 'reject':
                friend_request.status = RequestStatusEnum.Rejected.value
            else:
                return Response({'error': 'Invalid action'}, status=HTTP_400_BAD_REQUEST)

            friend_request.save()
            return Response({'message': f'Friend request {action}ed successfully'})
        except FriendShipRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=HTTP_404_NOT_FOUND)
        
class FriendsListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        friends = User.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status= RequestStatusEnum.Accepted.value) |
            Q(received_requests__from_user=user, received_requests__status=RequestStatusEnum.Accepted.value)
        ).distinct()
        return friends

class PendingFriendRequestsView(ListAPIView):
    serializer_class = FriendShipRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return FriendShipRequest.objects.filter(to_user=user, status= RequestStatusEnum.Pending.value)