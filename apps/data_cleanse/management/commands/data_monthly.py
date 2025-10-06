from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd

class Command(BaseCommand):
    help = "Split the processed prices.parquet data into monthly files."

    def handle(self, *args, **options):
        # 1. 입력 파일과 출력 폴더 경로 설정
        input_file = Path("data/processed/merged_final.parquet")
        # --- 수정된 부분 1: 출력 폴더를 'data/data_monthly/'로 변경 ---
        output_dir = Path("data/data_monthly/")

        # --- 수정된 부분 2: 출력 폴더가 없으면 자동으로 생성 ---
        # exist_ok=True 옵션은 폴더가 이미 있어도 오류를 발생시키지 않습니다.
        output_dir.mkdir(parents=True, exist_ok=True)

        if not input_file.exists():
            self.stderr.write(self.style.ERROR(f"Input file not found: {input_file}"))
            self.stderr.write("Please run 'python manage.py ingest_prices' first.")
            return

        self.stdout.write(f"Reading {input_file}...")
        df = pd.read_parquet(input_file)

        # 2. 'date' 컬럼이 있는지 확인하고 날짜 형식으로 변환
        if 'date' not in df.columns:
            self.stderr.write(self.style.ERROR("The 'date' column was not found in the Parquet file."))
            return
            
        # 날짜 형식을 자동으로 감지하여 날짜 타입으로 변환
        df['date'] = pd.to_datetime(df['date'])

        # 3. '연도-월'을 기준으로 데이터 그룹화
        grouped = df.groupby(pd.Grouper(key='date', freq='M'))
        
        total_files = len(grouped)
        self.stdout.write(f"Splitting data into {total_files} monthly files...")

        # 4. 각 월별 그룹을 별도의 Parquet 파일로 저장
        for i, (month_end_date, data_for_month) in enumerate(grouped, 1):
            year_month = month_end_date.strftime('%Y-%m')
            output_filename = f"merged_final_{year_month}.parquet"
            output_path = output_dir / output_filename

            if not data_for_month.empty:
                self.stdout.write(f"({i}/{total_files}) Saving {output_path}...")
                data_for_month.to_parquet(output_path, index=False)
            else:
                 self.stdout.write(f"({i}/{total_files}) Skipping empty month: {year_month}")

        self.stdout.write(self.style.SUCCESS(f"Successfully split all data into '{output_dir}' folder."))
