from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
from django.conf import settings

class Command(BaseCommand):
    help = "Ingest price data (CSV→Parquet) into data/processed"

    def add_arguments(self, parser):
        parser.add_argument("--source", default="csv", help="data source name")
        parser.add_argument("--path", default="data/merged_final.csv", help="csv path")

    def handle(self, *args, **opts):
        csv_path = Path(opts["path"])
        if not csv_path.exists():
            self.stderr.write(f"CSV not found: {csv_path}")
            return
        df = pd.read_csv(csv_path)
        out = Path("data/processed/merged_final.parquet")
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out, index=False)
        self.stdout.write(self.style.SUCCESS(f"Ingested → {out}"))
