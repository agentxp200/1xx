from django.contrib import admin
from . models import reg, notifications,scam, feedback,scammodel
# Register your models here.

admin.site.register(reg)
admin.site.register(scam)
admin.site.register(feedback)
admin.site.register(notifications)
admin.site.register(scammodel)

