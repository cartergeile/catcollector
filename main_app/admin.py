from django.contrib import admin

from .models import Cat, Feeding

# Register your models here.
admin.site.register(Cat)
#register our new feeding model
admin.site.register(Feeding)