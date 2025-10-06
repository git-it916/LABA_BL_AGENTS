from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd

class Command(BaseCommand):
    help = "Shows the first few rows (head) of a Parquet file."

    def add_arguments(self, parser):
        # 사용자가 파일 경로를 직접 지정할 수 있도록 옵션 추가
        parser.add_argument(
            "--path",
            default="data/merged_final_2015-01.parquet",
            help="Path to the Parquet file to inspect."
        )
        # 몇 줄을 볼지 사용자가 정할 수 있도록 옵션 추가
        parser.add_argument(
            "--rows",
            type=int,
            default=5,
            help="Number of rows to display."
        )

    def handle(self, *args, **options):
        file_path = Path(options["path"])
        num_rows = options["rows"]

        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            self.stdout.write(f"Peeking into {file_path}...")
            df = pd.read_parquet(file_path)

            # 데이터의 상위 N개 행을 보여줌 (df.head())
            self.stdout.write(f"Displaying the first {num_rows} rows:")
            
            # pandas 데이터프레임을 예쁘게 문자열로 출력
            # to_string()을 사용하면 모든 열이 잘리지 않고 표시됩니다.
            print(df.head(num_rows).to_string())

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))