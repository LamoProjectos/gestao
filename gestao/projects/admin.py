from django.contrib import admin
from .models import Project, ProjectStage, TemplateEtapa


class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 0
    fields = ['ordem', 'nome', 'data_prevista', 'concluida']
    ordering = ['ordem']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cliente', 'tipo', 'status', 'valor_total', 'data_entrega', 'progresso_percentual']
    list_filter = ['tipo', 'status', 'data_inicio', 'data_entrega']
    search_fields = ['nome', 'cliente__nome', 'descricao']
    inlines = [ProjectStageInline]


@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ['nome', 'projeto', 'ordem', 'data_prevista', 'concluida']
    list_filter = ['concluida', 'projeto']
    search_fields = ['nome', 'projeto__nome']


@admin.register(TemplateEtapa)
class TemplateEtapaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_projeto', 'ordem', 'dias_apos_inicio']
    list_filter = ['tipo_projeto']
    ordering = ['tipo_projeto', 'ordem']
