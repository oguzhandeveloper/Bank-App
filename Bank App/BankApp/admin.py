from django.contrib import admin
from .models import Havale
from .models import Tblhavaletip
from .models import Tblhesap
from .models import Tblhesapek
from .models import Tblkisi
from .models import Tblmusteri

# Register your models here.
admin.site.register(Havale)
admin.site.register(Tblhavaletip)
admin.site.register(Tblhesap)
admin.site.register(Tblhesapek)
admin.site.register(Tblkisi)
admin.site.register(Tblmusteri)
