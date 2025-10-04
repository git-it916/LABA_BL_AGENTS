from django.core.management.base import BaseCommand
from apps.backtest.engine import run_backtest

class Command(BaseCommand):
    help = "Run backtest using stored BL runs/weights"

    def add_arguments(self, parser):
        parser.add_argument("--run-id", type=int, required=False)

    def handle(self, *args, **opts):
        # TODO: load weights by run-id & simulate
        perf = run_backtest(None)
        self.stdout.write(self.style.SUCCESS(f"Backtest done: {perf}"))
