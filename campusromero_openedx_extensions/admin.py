from django.contrib.admin.sites import NotRegistered
from django.contrib import admin
from student.models import LoginFailures


class LoginFailuresAdmin(admin.ModelAdmin):
    """ Admin interface for the LoginFailures model. """
    raw_id_fields = ('user',)
    list_display = ('user', 'failure_count', 'lockout_until',)
    list_filter = ('lockout_until',)
    search_fields = ('user__username', 'user__email',)


try:
    admin.site.unregister(LoginFailures)
except NotRegistered:
    pass

admin.site.register(LoginFailures, LoginFailuresAdmin)
