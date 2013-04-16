from django import template
from django_fabv.models import Experiment, Test, Choice

register = template.Library()


@register.simple_tag(takes_context=True)
def variation(context, experiment_name):
    try:
        experiment = Experiment.objects.get(short_name=experiment_name)
        # If an experiment has a result always use that result
        if experiment.result is not None:
            content = experiment.result.content
        else:
            user = context['request'].fabv_user

            try:
                choice = Choice.objects.select_related(depth=1).\
                  filter(experiment=experiment).filter(user=user)[0]
                content = choice.test.content
            except:
                # If this is the first visit display a random variation
                test = Test.objects.\
                  filter(experiment__short_name=experiment_name).\
                  order_by('?')[0]
                content = test.content
                Choice.objects.create(experiment=experiment,
                                               test=test,
                                               user=user)
    except:
        # What is a good behavior here?
        content = ""
    return content
