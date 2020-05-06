import jwt
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS

from apps.autenticacion.managers import CustomUserManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('nombre de usuario'), max_length=30, unique=True)
    email = models.EmailField(_('correo electronico'), unique=True)
    is_staff = models.BooleanField(_('Acceso al Sitio Administrativo'), default=False)
    is_active = models.BooleanField(_('Activar usuario'), default=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    nombres = models.CharField(_('nombres'), blank=True, max_length=40)
    apellidos = models.CharField(_('Apellidos'), blank=True, max_length=40)
    token_firebase = models.CharField(_('TokenFirebase'),max_length=255,blank=True,null=True)
    foto = models.ImageField(upload_to='perfiles/', default = 'perfiles/no-img.jpg', blank=True, null=True)
    groups = models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.Group', 
        verbose_name='grupos1',db_table='USUARIO_GRUPO',
        help_text='Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los '
                'permisos otorgados a cada uno de sus grupos.')
    user_permissions = models.ManyToManyField(blank=True, help_text='Permisos específicos para este usuario.', 
        related_name='user_set', related_query_name='user',to='auth.Permission', verbose_name='user permissions',
        db_table='USUARIO_PERMISO')
        
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = CustomUserManager()

    class Meta:
        db_table = 'USUARIO'
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
    
    def __str__(self):
        return self.username
    
    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username
    
    def grupos(self):
        return self.groups.filter().values('name')

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    telefono = models.IntegerField(blank=True,null=True)
    calificacion = models.IntegerField(default=0)
    disponibilidad = models.CharField(max_length=1, default='N',choices=(
		('L','Libre'),('O', 'Ocupado'),('N', 'No Disponible')
	))

    class Meta:
        ordering = ['usuario']
        db_table = 'PERFIL'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return '%s' % (self.usuario)