from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CropRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    crop_result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):

    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('lab', 'Lab'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='farmer')
    location = models.CharField(max_length=150)

    def __str__(self):
        return self.user.username

    

from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SoilTestRequest(models.Model):
    lab_name = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)
    appointment = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lab_name} - {self.soil_type}"
    



from django.db import models
from django.contrib.auth.models import User


class FertilizerHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    temperature = models.FloatField()
    humidity = models.FloatField()
    moisture = models.FloatField()

    soil_type = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=100)

    nitrogen = models.FloatField()
    phosphorous = models.FloatField()
    potassium = models.FloatField()

    prediction = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


class YieldHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    crop = models.CharField(max_length=100)
    crop_year = models.IntegerField()
    season = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    area = models.FloatField()
    annual_rainfall = models.FloatField()
    fertilizer = models.FloatField()
    pesticide = models.FloatField()

    prediction = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.crop}"
    



class SoilTestRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    lab_name = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)

    appointment_date = models.DateTimeField()

    notes = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username