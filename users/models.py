from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.conf import settings
from django.db import models

import africastalking as at

AFRICAS_TALKING = settings.AFRICAS_TALKING

at.initialize('glitex', AFRICAS_TALKING)

sms = at.SMS


GENDER = (
    ("None", "None"),
    ("Male", "Male"),
    ("Female", "Female")
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address!')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    image = models.ImageField(
        upload_to='users/%Y/%m', 
        null=True, 
        blank=True
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(
        max_length=15,
        null=True, 
        blank=True
    )
    phone_number = models.CharField(
        max_length=15,
        null=True, 
        blank=True
    )
    device_id = models.CharField(
        max_length=255,
        null=True, 
        blank=True
    )
    gender = models.CharField(
        choices=GENDER,
        default="None",
        max_length=6,
    )
    age = models.IntegerField(default=0)
    otp_code = models.IntegerField(default=0)

    phone_otp_registration = models.BooleanField(default=False)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    formater_address = models.CharField(
        max_length=255,
        null=True, 
        blank=True
    )

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creation_time',]

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def send_phonenumber_opt(self):
        otp = self.otp_code
        message = f"Your Account Confirmation OTP code is: {otp}"
        num = self.phone_number
        try:
            sms_msg = sms.send(message, [num], "Glitex")
            print(sms_msg)
            return True
            
        except Exception as e:
            print(f"{e}")
            return False
    
    def send_otp(self):
        return send_mail(
            "Confirmation OTP",
            f"Your account confirmation OTP code is: {self.otp_code}",
            "support@forge.com",
            [self.email],
            fail_silently=True
        )
    
    def send_password_change_email(self, password):
        return send_mail(
            "Password Change Alert",
            f"Your password has been chamged to {password}, make sure to change it to a secure one.",
            "support@forge.com",
            [self.email],
            fail_silently=True
        )
    
    def update_user_password(self, password):
        self.set_password(password)
        self.otp_code = 0
        return self.save()
    

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    document = models.FileField(
        upload_to='profile/%Y/%m', 
        null=True, 
        blank=True
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creation_time',]

    def __str__(self):
        return self.user.email
    

@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    """
    creates a profile after user is saved
    """
    if created:
        Profile.objects.create(
            user=instance
        )
        if not instance.phone_otp_registration:
            if not  instance.is_superuser:
                instance.send_otp()