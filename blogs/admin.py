from django.contrib import admin

from .models import *

admin.site.register(Blog)
admin.site.register(BlogLike)
admin.site.register(BlogComment)
admin.site.register(PreviewImage)
