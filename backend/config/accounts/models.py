from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email not added")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', 'User'
        OWNER = 'owner', 'Owner'
        ADMIN = 'admin', 'Admin'

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} has {self.role}"
    
class Venue(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        SUSPENDED = 'suspended', 'Suspended'

    owner = models.ForeignKey(User, 
                              on_delete=models.PROTECT, 
                              related_name="owned_venues")
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.PositiveIntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length = 20,
        choices = Status.choices,
        default = Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    approved_by = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name="approved_venues")

    def __str__(self):
        return f"{self.name} in {self.location} has {self.price_per_hour} with {self.status}"
    
class Gallery(models.Model):
    venue = models.ForeignKey(Venue,
                              on_delete=models.CASCADE,
                              related_name="photos")
    image = models.ImageField(upload_to="venue_galleries/")
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.venue.name}"