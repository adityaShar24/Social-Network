from django.db import models
from UserAuthentication.models import User
from datetime import datetime, timedelta
from .enums import RequestStatusEnum

class FriendShipRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=RequestStatusEnum.choices(),
        default=RequestStatusEnum.Pending.value
                            )
    
    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"