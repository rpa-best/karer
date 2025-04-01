from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

ROLE_MANAGER = 'manager'
ROLE_LOGIST = 'logist'

ROLES = (
    (ROLE_MANAGER, ROLE_MANAGER),
    (ROLE_LOGIST, ROLE_LOGIST)
)


class User(AbstractUser):
    role = models.CharField(max_length=255, blank=True, null=True, choices=ROLES)
    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True, null=True,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _("email address"),
        blank=True, null=True,
        unique=True
    )

    def __str__(self):
        return self.username or self.email

    def clean(self) -> None:
        if not self.username:
            self.username = None
        if not self.email:
            self.email = None

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        constraints = [
            models.CheckConstraint(
                name=_("username or email"),
                check=(
                    models.Q(username__isnull=False) | models.Q(email__isnull=False)
                ),
            )
        ]