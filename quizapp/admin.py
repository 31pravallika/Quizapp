from django.contrib import admin
from .models import Category
from .models import Questions
from .models import Options
from .models import correctopt
from .models import useropt
from .models import testtaken
# Register your models here.
admin.site.register(Category)
admin.site.register(Questions)
admin.site.register(Options)
admin.site.register(correctopt)
admin.site.register(useropt)
admin.site.register(testtaken)