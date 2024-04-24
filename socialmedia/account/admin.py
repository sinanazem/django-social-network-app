from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.register(Relation)
admin.site.unregister(User)
admin.site.register(User, ExtendUserAdmin)

