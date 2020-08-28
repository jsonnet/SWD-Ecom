from django.contrib import admin

from .models import *

admin.site.register(UserProfile)
admin.site.register(Partner)
admin.site.register(Product)
admin.site.register(PWResetToken)

