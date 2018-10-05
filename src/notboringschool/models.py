from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import transaction, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    @transaction.atomic
    def create_inactive_user(self, email, **extra_fields):

        if not email:
            raise ValueError(_('Users must have an email address'))
        try:
            user = self.get(email=email)
        except self.model.DoesNotExist as e:
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.is_active = False
            user.is_staff = False
            user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('email'), max_length=254, unique=True)
    date_joined = models.DateTimeField(verbose_name=_("Date joined"), default=timezone.now)
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=512, blank=True, default='')
    phone = models.CharField(verbose_name=_("Phone"), max_length=250, blank=True, default='')

    is_send_email = models.BooleanField(verbose_name=_('send email'), default=False)
    send_email_date = models.DateTimeField(verbose_name=_("Date send activation email"), blank=True, null=True)

    is_staff = models.BooleanField(verbose_name=_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(verbose_name=_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
