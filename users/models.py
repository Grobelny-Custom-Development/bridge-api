from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)
from django.db import models
from uuid import uuid4

from bridge.model_utility import TimeStampAbstractMixin


class GenericUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        self.is_staff = False
        self.is_admin = True
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        self.is_staff = True
        self.is_admin = True
        return self._create_user(email, password, **extra_fields)
class AbstractGenericUser(AbstractBaseUser, TimeStampAbstractMixin):

    class Meta:
        abstract = True

class GenericUser(AbstractGenericUser):
    email = models.EmailField(
        max_length=255,
        unique=True)

    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=2,null=True, blank=True)


    # used to denote whether this is someone who can acces ORM directly
    is_admin = models.BooleanField(default=False, blank=True)
    # if need to deactivate specific accounts
    is_active = models.BooleanField(default=True, blank=True)
    USERNAME_FIELD = 'email'
    # could be used for 2FA at some point, useful to collect
    phone_number = models.CharField(max_length=10, null=True)
    # use for external applications/more secure identifier
    user_uuid = models.UUIDField(default=uuid4, editable=False)
    # TODO:: discuss delete policy here but would assume users stay intact
    company_id = models.ForeignKey('Company',
                                    models.SET_NULL,
                                    blank=True,
                                    null=True,)

    objects = GenericUserManager()

# TODO::figure out what other info we need to store at the company level
class Company(TimeStampAbstractMixin):
    name = models.CharField(max_length=40)

    # date that company started using bridge
    effective_start = models.DateTimeField(null=True, blank=True)
    # date that company stopped using bridge
    effective_end = models.DateTimeField(null=True, blank=True)

    company_uuid = models.UUIDField(default=uuid4, editable=False)