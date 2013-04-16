from __future__ import absolute_import
from collections import namedtuple
from django.core.management.base import BaseCommand, CommandError
from ...models import Experiment, Test
from ...helpers import get_data
from ...statistics import test, describe

Alternative = namedtuple("Alternative", ['participants', 'hits'])


class Command(BaseCommand):
    """
    Implements the fabv commands
    """

    def handle(self, *args, **options):
        """
        Handles a command
        """
        if len(args) == 0:
            self.print_help()
        else:
            if args[0] == 'help':
                self.print_help()
            elif args[0] == 'list':
                self.list()
            elif args[0] == 'show':
                if len(args) == 1:
                    self.show_help()
                else:
                    self.show(args)
            elif args[0] == 'choose':
                if len(args) == 1:
                    self.choose_help()
                elif len(args) == 3:
                    self.choose(args)
                else:
                    raise CommandError(
                        "'choose' requires exactly 2 arguments.")
            elif args[0] == 'calculate':
                if len(args) == 2:
                    self.calculate(args)
                else:
                    raise CommandError(
                        "'calculate' requires exactly 1 argument.")
            else:
                raise CommandError("'%s' is an unknown command" % args[0])

    def calculate(self, args):
        """
        Calculate the results for an experiment and print it
        """
        try:
            alternatives = get_data(args[1])
            (p, best, worst) = test(alternatives)
            describe(alternatives, p, best, worst)

        except Test.DoesNotExist:
            raise CommandError("Experiment not found")
        except ValueError:
            raise CommandError(ValueError.message)

    def choose(self, args):
        """
        Save the choice to the database
        """
        try:
            test = Test.objects.select_related().get(pk=args[2])
            if test.experiment.id != int(args[1]):
                if Experiment.objects.filter(pk=args[1]).count() > 0:
                    raise CommandError(
                        "Experiment does not match alternative.")
                else:
                    raise CommandError("Experiment not found.")
            else:
                test.experiment.result = test
                test.experiment.save()
                raise CommandError("%s chosen." % test)

        except Test.DoesNotExist:
            raise CommandError("Alternative not found.")

    def choose_help(self):
        """
        Display the help on choosing an alternative
        """
        print "Force the display of one of the alternatives."

    def show(self, args):
        """
        Shows info on all experiments designated in args

        TODO: Add selection on short names.
        """
        for arg in args[1:]:
            self.show_experiment(arg)

    def show_experiment(self, id):
        """
        Show information on an experiment
        """
        try:
            experiment = Experiment.objects.select_related().get(pk=id)
            print experiment
            alternatives = experiment.test_set.get_query_set()
            if len(alternatives) > 0:
                print "\nAlternatives:"
                for alternative in alternatives:
                    print "\t- %s with ID: %s" % (alternative, alternative.pk)
        except Experiment.DoesNotExist:
            print "Experiment %s not found" % id
        print

    def show_help(self):
        """
        Displays help regarding the show command
        """
        print "Shows information on an experiment identified by ID."

    def list(self):
        """
        Lists all experiments
        """
        has_experiments = False

        experiments = Experiment.objects.all()
        for experiment in experiments:
            has_experiments = True
            print "ID\tDescription"
            print "%s\t%s" % (experiment.pk, experiment)

        if not has_experiments:
            print "No experiments configured."

    def print_help(self):
        """
        Prints the help message
        """
        print """fabv supports the following commands:

help\t\t\tPrints this message
list\t\t\tLists all experiments
show <ID>, ...\t\tShow info on one or more experiments
choose <ID> <aID>\tChoose an alternative for the experiment with ID
\t\t\t<ID> and alternative with ID aID
calculate <ID>\t\tCalculate the statistics for the experiment with id
\t\t\t<ID>"""
