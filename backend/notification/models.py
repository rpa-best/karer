from django.db import models

SEVERITY_SUCCESS = 'success'
SEVERITY_DANGER = 'danger'
SEVERITY_INFO = 'info'

SEVERITIES = (
    (SEVERITY_SUCCESS, SEVERITY_SUCCESS),
    (SEVERITY_DANGER, SEVERITY_DANGER),
    (SEVERITY_INFO, SEVERITY_INFO)
)

class Notification(models.Model):
    user = models.ForeignKey('oauth.User', models.CASCADE)
    label = models.CharField(max_length=255)
    message = models.TextField()
    redirect_url = models.URLField(blank=True, null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    severity = models.CharField(max_length=20, choices=SEVERITIES)

    def __str__(self):
        return self.message
