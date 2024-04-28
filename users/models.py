from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



CUSTOMER,EMPLOYEE,ADMIN = ('customer','employee', 'admin')


class User(AbstractUser,BaseModel):

    USER_ROLES = (
        (CUSTOMER,CUSTOMER),
        (EMPLOYEE, EMPLOYEE),
        (ADMIN,ADMIN)

    )
    manzil=models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=13,unique=True, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    user_role = models.CharField(max_length=25, choices=USER_ROLES, default=CUSTOMER)
    email = models.CharField(max_length=100, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='user_images/',
    validators=[FileExtensionValidator(allowed_extensions=['jpeg','png','jpg'])], null=True, blank=True)


    def __str__(self):
        return self.username
    

    
    