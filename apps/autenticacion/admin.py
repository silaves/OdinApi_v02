from django.contrib import admin
from django import forms
# Register your models here.
from django.contrib.admin.widgets import AdminTimeWidget
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.db.models.sql.datastructures import Join

from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupForm
from .models import Usuario, Perfil, Horario


class PerfilInline(admin.StackedInline):
    model = Perfil
    fields = ('telefono', 'calificacion','disponibilidad' )
    readonly_fields = ('calificacion',)
    can_delete = False

class HorarioForm(forms.ModelForm):
    entrada = forms.TimeField(widget=AdminTimeWidget(format='%H:%M'))

    class Meta:
        model = Horario
        fields = '__all__'
    
    def clean(self):
        entrada = self.cleaned_data.get('entrada')
        salida = self.cleaned_data.get('salida')
        if entrada and salida:
            if entrada > salida:
                raise forms.ValidationError({'entrada':['El horario de entrada no puede ser mayor al de salida']})
            elif entrada == salida:
                raise forms.ValidationError({'entrada':['El horario de entrada no puede ser igual al de salida']})
        return self.cleaned_data


class HorarioInline(admin.StackedInline):
    model = Horario
    form = HorarioForm
    fields = ('entrada', 'salida','estado' )
    can_delete = False
    extra = 1

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ('id','username', 'nombres', 'apellidos', 'is_staff', 'is_active', 'get_groups', 'last_login')
    list_filter = ('username', 'is_staff', 'is_active', 'groups')
    fieldsets = (
        ('Informacion Personal', {'fields': ('username', 'password', 'nombres', 'apellidos','email','foto','ciudad')}),
        ('Permisos', {'fields': ('is_staff', 'is_active','groups', 'user_permissions')}),
    )
    add_fieldsets =(        
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'nombres',  'apellidos', 'foto','email', 'is_staff', 'is_active')}
        ),
    )
    inlines = (PerfilInline, HorarioInline,)
    search_fields = ('username',)
    ordering = ('username',)
    actions = ["activar_usuario"]

    class Media:
        js = ['own/js/admin.js']

    def get_actions(self, request):#eliminar la accion de eliminar
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def activar_usuario(self, request, queryset):#acciones masivas
        queryset.update(is_active=True)

    def get_groups(self, obj):
        print(obj)
        print("*-*-*-*-*-*-*-")
        #qs = Group.objects.filter(CustomUser.username = obj)
        #print(qs)
        q1 = Usuario.objects.get(username = obj)
        q2 = Group.objects.filter(user=q1)
        str_groups = ""
        for p in q2:
            str_groups += p.name+", "
        if str_groups=="":
            return ""
        else:
            return str_groups[:len(str_groups)-2]


class GroupAdmin(admin.ModelAdmin):
    form = GroupForm
    model = Group
    search_fields = ('name',)
    ordering = ('name',)



admin.site.register(Usuario, CustomUserAdmin)
# admin.site.register(Permission)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)