from django.core.management.base import BaseCommand
from apps.agents.generators import generate_views_from_news

class Command(BaseCommand):
    help = "Generate BL views (P,q,Omega) using LLM/news"

    def add_arguments(self, parser):
        parser.add_argument("--as-of", required=True)

    def handle(self, *args, **opts):
        views = generate_views_from_news(opts["as_of"])
        self.stdout.write(self.style.SUCCESS(f"Generated {len(views)} views for {opts['as-of']}"))
