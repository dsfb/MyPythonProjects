from django.contrib import admin
from .models import Comentarios, Cursos, Aulas, NotasAulas

admin.site.register(Aulas)
admin.site.register(Cursos)
admin.site.register(Comentarios)
admin.site.register(NotasAulas)
