from django.db import models


# Create your models here.
class ArgyleAPIKeys(models.Model):
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    plugin_key = models.CharField(max_length=100)
    # Determines whether the keys are from sandbox or production
    is_sandbox_mode = models.BooleanField(default=False)

    @staticmethod
    def get_argyle_keys():
        return ArgyleAPIKeys.objects.first()
