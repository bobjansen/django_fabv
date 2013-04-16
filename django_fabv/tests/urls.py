from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.simple',
                       (r'^$', 'direct_to_template',
                        {'template': 'index.html'}),
                       (r'^test/$', 'direct_to_template',
                        {'template': 'test.html'}),
                       (r'^landing/$', 'direct_to_template',
                        {'template': 'landing.html'}),
                       (r'^signup/$', 'direct_to_template',
                        {'template': 'signup.html'}),
                       (r'^persistence/$', 'direct_to_template',
                        {'template': 'persistence.html'}),
                       )
