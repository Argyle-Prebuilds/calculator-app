from datetime import datetime

from django.db import models

TOKEN_ACTIVE = 'active'
TOKEN_EXPIRED = 'expired'


class ArgyleUser(models.Model):
    argyle_id = models.UUIDField(unique=True)
    token_expiry = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    first_name = models.CharField(blank=True, null=True, max_length=50)
    last_name = models.CharField(blank=True, null=True, max_length=50)

    def get_token_status(self):
        now_timestamp = datetime.timestamp(datetime.now())
        if self.token_expiry > now_timestamp:
            return TOKEN_ACTIVE
        return TOKEN_EXPIRED
