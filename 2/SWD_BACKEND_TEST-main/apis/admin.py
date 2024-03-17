from django.contrib import admin
from .models import SchoolStructure
from .models import Schools
from .models import Classes
from .models import Personnel
from .models import Subjects
from .models import StudentSubjectsScore

admin.site.register(SchoolStructure)
admin.site.register(Schools)
admin.site.register(Classes)
admin.site.register(Personnel)
admin.site.register(Subjects)
admin.site.register(StudentSubjectsScore)