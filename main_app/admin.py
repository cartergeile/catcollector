from django.contrib import admin

from .models import Cat, Feeding, Toy, Photo

# Register your models here.
admin.site.register(Cat)
#register our new feeding model
admin.site.register(Feeding)
# register toy model
admin.site.register(Toy)
# register photo model
admin.site.register(Photo)