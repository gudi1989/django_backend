"""
There are three roles available to check for when using ``user.has_perm(...)``.

- ``auth.editor_permission``
- ``auth.chief_editor_permission``
  (includes all permissions that ``editor_permission`` has).
- ``auth.admin_permission``
  (includes all permissions that ``chief_editor_permission`` has).
"""

import re

from django.contrib.auth import get_permission_codename
import django_callable_perms
from django_callable_perms import register


class BaseModelBackendPermissions(object):
    """
    A class-based approach to registering model permissions with
    django_callable_perms.

    To add a new object-level permission create a subclass of this and add a
    method with the name ``check_<perm-name>_object_permission``. This will
    register this method as a check with django_callable_perms where the
    permission name is ``<perm-name>`` put into context of the model passed
    into the `__init__` method.

    For instance, if you pass the ``auth.User`` model and have a
    ``check_read_object_permission`` method, the actuall permission name will
    be ``auth.read_user``.

    You can also add non-object-level permission checks with the naming scheme
    for methods: ``check_<perm-name>_permission``.

    If you want to use a different permission name than what is used in the
    method's name, then attach the ``permission_name`` attribute of the method,
    for example::

        def check_read_permission(self, user, perm, obj):
            return True
        check_read_permission.permission_name = 'my_app.access_model'
    """

    def __init__(self, model):
        self.model = model
        self.registered = False

    def get_permission_name(self, perm):
        if '.' in perm:
            return perm
        return '{app_label}.{permission_name}'.format(
            app_label=self.model._meta.app_label,
            permission_name=get_permission_codename(perm, self.model._meta))

    def get_permission_checks(self):
        permission_re = re.compile('^check_(.+?)(?!_object)_permission$')
        permissions = []
        for attr in dir(self):
            match = permission_re.match(attr)
            if match:
                permission_name = match.groups()[0]
                check = getattr(self, attr)
                # Get attribute of check to find out the permission name that
                # shall be used for this check.
                permission_name = getattr(check, 'permission_name', permission_name)
                permission_name = self.get_permission_name(permission_name)
                permissions.append((permission_name, check))
        return permissions

    def get_object_permission_checks(self):
        permission_re = re.compile('^check_(.+?)_object_permission$')
        permissions = []
        for attr in dir(self):
            match = permission_re.match(attr)
            if match:
                permission_name = match.groups()[0]
                check = getattr(self, attr)
                # Get attribute of check to find out the permission name that
                # shall be used for this check.
                permission_name = getattr(check, 'permission_name', permission_name)
                permission_name = self.get_permission_name(permission_name)
                permissions.append((permission_name, check))
        return permissions

    def register(self):
        if self.registered:
            raise RuntimeError(
                'You already tried to register {0}. You can only do this '
                'once.'.format(self))

        for permission, check in self.get_permission_checks():
            django_callable_perms.register(permission, check)
        for permission, check in self.get_object_permission_checks():
            django_callable_perms.register(permission, check, self.model)
        self.registered = True


class ModelBackendPermissions(BaseModelBackendPermissions):
    """
    Default permissions that need to exist in order to use the backend.
    """

    def check_list_permission(self, user, perm, obj):
        return user.has_perm('auth.editor_permission')

    def check_viewlog_permission(self, user, perm, obj):
        return user.has_perm('auth.editor_permission')

    def check_read_permission(self, user, perm, obj):
        return user.has_perm('auth.editor_permission')

    def check_read_object_permission(self, user, perm, obj):
        return self.check_read_permission(user, perm, obj)

    def check_add_permission(self, user, perm, obj):
        return user.has_perm('auth.editor_permission')

    def check_change_permission(self, user, perm, obj):
        return user.has_perm('auth.editor_permission')

    def check_change_object_permission(self, user, perm, obj):
        return self.check_change_permission(user, perm, obj)

    def check_delete_permission(self, user, perm, obj):
        return user.has_perm('auth.editor_permission')

    def check_delete_object_permission(self, user, perm, obj):
        return self.check_delete_permission(user, perm, obj)


#
# Base permissions, for all backends.


def may_access_backend(user, perm, obj):
    return user.has_perm('auth.editor_permission')


register(
    'django_backend.access_backend',
    may_access_backend)

