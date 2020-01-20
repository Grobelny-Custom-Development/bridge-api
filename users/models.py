from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
)
from django.db import models
from uuid import uuid4
import datetime

from bridge.model_utility import TimeStampAbstractMixin


class GenericUserManager(BaseUserManager):
    """Define a model manager for User model with an email as username."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.last_login = datetime.datetime.now()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        user = self._create_user(email, password, **extra_fields)
        user.is_staff = False
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        user = self._create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user
class AbstractGenericUser(AbstractBaseUser, TimeStampAbstractMixin):

    class Meta:
        abstract = True

class GenericUser(AbstractGenericUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(
        max_length=255,
        unique=True)

    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=2,null=True, blank=True)


    # used to denote whether this is someone who can acces ORM directly
    # both are needed by django
    is_admin = models.BooleanField(default=False, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)

    # if need to deactivate specific accounts
    is_active = models.BooleanField(default=True, blank=True)
    
    # could be used for 2FA at some point, useful to collect
    phone_number = models.CharField(max_length=10, null=True)
    # use for external applications/more secure identifier
    user_uuid = models.UUIDField(default=uuid4, editable=False)
    # TODO:: discuss delete policy here but would assume users stay intact
    company = models.ForeignKey('Company',
                                    models.SET_NULL,
                                    blank=True,
                                    null=True,)

    objects = GenericUserManager()
    
    def get_short_name(self):
        # Return user's primary identifier
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True


# TODO::figure out what other info we need to store at the company level
class Company(TimeStampAbstractMixin):
    name = models.CharField(max_length=40)

    # date that company started using bridge
    effective_start = models.DateTimeField(null=True, blank=True)
    # date that company stopped using bridge
    effective_end = models.DateTimeField(null=True, blank=True)
    # external uuid 
    company_uuid = models.UUIDField(default=uuid4, editable=False)

    def save(self, *args, **kwargs):
        # if we haven't set the uuid then set it now as long as it's not already in the table
        if not self.company_uuid:
            uuid = uuid4()
            while Company.objects.filter(company_uuid=uuid).exists():
                uuid = uuid4()

            self.uuid = uuid
        super(Company, self).save(*args, **kwargs)

