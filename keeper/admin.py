from django.contrib import admin
from .models import usr_token

@admin.register(usr_token)
class usr_tokenAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'token',
        'user',
    ]