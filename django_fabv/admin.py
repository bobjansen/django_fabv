from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext as _
from django.db.models import Q
from models import Experiment, Test, User, Hit, Goal, Choice

# Taken from: http://www.bingocardcreator.com/abingo/faq
BOTS = bots = ['Baidu', 'Gigabot', 'Googlebot', 'libwww-perl', 'lwp-trivial',
               'msnbot', 'SiteUptime', 'Slurp', 'WordPress', 'ZIBB', 'ZyBorg']


class UserAgentFilter(SimpleListFilter):
    title = _('User Agent')

    parameter_name = 'useragent'

    def lookups(self, request, model_admin):
        return (
            ('No bots', _('No bots')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'No bots':
            # From http://stackoverflow.com/a/7088229/862288
            return queryset.exclude(
                reduce(lambda x, y: x | y,
                       [Q(user_agent__contains=bot) for bot in BOTS]))


class StatusCodeFilter(SimpleListFilter):
    title = _('HTTP Status code')

    parameter_name = 'statuscode'

    def lookups(self, request, model_admin):
        return (
            ('200 only', _('200 only')),
            ('Errors', _('Errors')),
            ('Redirects', _('Redirects')),
        )

    def queryset(self, request, queryset):
        if self.value() == '200 only':
            return queryset.filter(status_code="200")

        if self.value() == 'Errors':
            return queryset.filter(Q(status_code__startswith="4") |
                                   Q(status_code__startswith="5"))

        if self.value() == 'Redirects':
            return queryset.filter(status_code__startswith="3")


class UserFilter(SimpleListFilter):
    title = _('Logged in visitors')

    parameter_name = _('Visitors')

    def lookups(self, request, model_admin):
        return (
            ('in', _('Logged in users')),
            ('out', _('Anonymous users')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'in':
            return queryset.exclude(username__exact="")

        if self.value() == 'out':
            return queryset.filter(username__exact="")


class HitAdmin(admin.ModelAdmin):
    list_filter = (UserAgentFilter, StatusCodeFilter, UserFilter, )


class TestInline(admin.StackedInline):
    model = Test
    extra = 1


class ExperimentAdmin(admin.ModelAdmin):
    inlines = [TestInline]

admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(User)
admin.site.register(Hit, HitAdmin)
admin.site.register(Goal)
admin.site.register(Choice)
