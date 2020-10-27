from django.contrib import admin
from .models import FSI_user,Post,Comments,Project
# Register your models here.
admin.site.register(FSI_user)
admin.site.register(Project)
admin.site.register(Post)
admin.site.register(Comments)

