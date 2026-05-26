from django.contrib import admin

from .models import CropRecommendation
from .models import Profile
from django.contrib import admin
from .models import ContactMessage


admin.site.register(Profile)
admin.site.register(CropRecommendation)
from .models import FertilizerHistory
admin.site.register(ContactMessage)
admin.site.register(FertilizerHistory)