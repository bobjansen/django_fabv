from django.db import models
from django.utils.translation import ugettext as _


class Experiment(models.Model):
    """
    An experiment with goals and tests.
    """
    name = models.CharField(max_length=255,
                            help_text=_("The name of the experiment"))
    # Should be short, could be long
    short_name = models.CharField(max_length=255,
                                  help_text=_('The name used in template, ' +
                                  'use with {% variation "short_name" %}'))
    result = models.ForeignKey('Test', related_name='result',
                               null=True, blank=True,
                               help_text=_("The result of this experiment"))
    goal = models.OneToOneField('Goal', null=True, blank=True,
                                help_text=_("The conversion goal"))

    def __unicode__(self):
        """
        Shows the current state of this experiment
        """
        if self.result is None:
            return self.name + " (" + self.short_name + "): " + \
              _("No result yet")
        else:
            if self.result.p_value is None:
                return self.name + " (" + self.short_name + \
            "):" + _("The result is" + " ") + self.result.name
            else:
                return self.name + " (" + self.short_name + \
                  "): " + _("The result is" + " ") + self.result.name + \
                  " " + _("with score") + " " + str(self.result.p_value)


class Goal(models.Model):
    """
    Allow for multiple goals in the same category.
    """
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255,
                           help_text="The goal to convert to, can be a regex")
    #category = models.IntegerField(help_text="Ordinal")

    def __unicode__(self):
        return self.name + " " + _("for URL:") + " " + self.url


class Test(models.Model):
    """
    A version of an element.
    """
    experiment = models.ForeignKey(Experiment)
    name = models.CharField(max_length=255)
    content = models.TextField()
    p_value = models.FloatField(null=True, blank=True)

    def show(self):
        return self.content

    def __unicode__(self):
        return self.name + " " + _("for") + " " + self.experiment.name


class User(models.Model):
    """
    Holds a user identified by his key.

    All clients from the same IP will be assigned the same key.
    """
    key = models.CharField(max_length=64, db_index=True)
    ip = models.IPAddressField(db_index=True)

    def __unicode__(self):
        return _("User with key %s and ip %s") % (self.key, self.ip)


class Hit(models.Model):
    """
    Registers a hit on a url.

    Conversions are calculated from the Goals and the Choices.
    """
    user = models.ForeignKey(User)
    path = models.CharField(max_length=200)
    username = models.CharField(max_length=30, blank=True)
    status_code = models.IntegerField()
    referer = models.CharField(max_length=200)
    user_agent = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        if self.username == "":
            return _("Hit on %s from (%s, %s)") % (self.path,
                                                   self.user.ip, self.user.key)
        else:
            return _("Hit on %s from user %s (%s, %s)") % (self.path,
                                                           self.username,
                                                           self.user.ip,
                                                           self.user.key)


class Choice(models.Model):
    """
    Holds a choice for an experiment for a given user (key).
    """
    experiment = models.ForeignKey(Experiment)
    test = models.ForeignKey(Test)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return _("Choice for: %s in %s") % (self.user, self.experiment)
