from django.contrib import admin
from service.models import OutgoingRequests, IngoingRequests

# Register your models here.
admin.site.register(OutgoingRequests)
admin.site.register(IngoingRequests)