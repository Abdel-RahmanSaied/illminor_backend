from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(USERS)
admin.site.register(bloodTest)
admin.site.register(diabtesTest)
admin.site.register(parkinsonTest)
admin.site.register(alzhimarTest)
admin.site.register(heartTest)
admin.site.register(chestTest)
