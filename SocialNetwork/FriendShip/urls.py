from django.urls import path
from .views import FriendRequestView, FriendRequestResponseView, FriendsListView, PendingFriendRequestsView


urlpatterns = [
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:request_id>/<str:action>/', FriendRequestResponseView.as_view(), name='friend-request-response'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]