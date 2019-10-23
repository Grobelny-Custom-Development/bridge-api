from django.contrib.auth.models import (
    UserManager, BaseUserManager, AbstractBaseUser,
)
from django.db import models
from uuid import uuid4

from bridge.model_utility import TimeStampAbstractMixin

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

# TODO::figure out what other info we need to store at the company level
class Company(TimeStampAbstractMixin):
    name = models.CharField(max_length=40)

    # date that company started using bridge
    effective_start = models.DateTimeField(null=True, blank=True)
    # date that company stopped using bridge
    effective_end = models.DateTimeField(null=True, blank=True)

    company_uuid = models.UUIDField(default=uuid4, editable=False)