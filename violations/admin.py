from django.contrib import admin

from .models import User, Violations, ViolationSelection, Result

admin.site.register(User)
admin.site.register(Violations)
admin.site.register(ViolationSelection)
admin.site.register(Result)
