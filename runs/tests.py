from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


class TestSyncAllRunsCommand(TestCase):
    pass
#
#    @mock('runkeeper....')
#    def test_syn_all_runs_output(self):
#        out = StringIO()
#        call_command('syncallruns', stdout=out)
#        self.assertIn('XXXXX', out.getvalue())
