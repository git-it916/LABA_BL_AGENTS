from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd

class Command(BaseCommand):
    help = "Split the processed prices.parquet data into monthly files."

    def handle(self, *args, **options):
        # 1. 입력 파일과 출력 폴더 경로 설정
        input_file = Path("data/processed/merged_final.parquet")
        output_dir = Path("data/")

        if not input_file.exists():
            self.stderr.write(self.style.ERROR(f"Input file not found: {input_file}"))
            self.stderr.write("Please run 'python manage.py ingest_prices' first.")
            return

        self.stdout.write(f"Reading {input_file}...")
        df = pd.read_parquet(input_file)

        # 2. 'date' 컬럼이 있는지 확인하고 날짜 형식으로 변환
        #    (만약 날짜 컬럼 이름이 다르다면 이 부분을 수정해야 합니다)
        if 'date' not in df.columns:
            self.stderr.write(self.style.ERROR("The 'date' column was not found in the Parquet file."))
            return
            
        # YYYYMMDD 형식의 정수를 날짜 타입으로 변환
        df['date'] = pd.to_datetime(df['date'])

        # 3. '연도-월'을 기준으로 데이터 그룹화
        # df.groupby()는 데이터를 특정 기준으로 묶어주는 강력한 기능입니다.
        # pd.Grouper(key='date', freq='M')는 'date' 컬럼을 기준으로 월(Month) 단위로 그룹을 만듭니다.
        grouped = df.groupby(pd.Grouper(key='date', freq='M'))
        
        total_files = len(grouped)
        self.stdout.write(f"Splitting data into {total_files} monthly files...")

        # 4. 각 월별 그룹을 별도의 Parquet 파일로 저장
        for i, (month_end_date, data_for_month) in enumerate(grouped, 1):
            # 파일 이름 형식 지정 (예: 2023-01)
            year_month = month_end_date.strftime('%Y-%m')
            output_filename = f"merged_final_{year_month}.parquet"
            output_path = output_dir / output_filename

            # 데이터가 비어있지 않은 경우에만 저장
            if not data_for_month.empty:
                self.stdout.write(f"({i}/{total_files}) Saving {output_path}...")
                data_for_month.to_parquet(output_path, index=False)
            else:
                 self.stdout.write(f"({i}/{total_files}) Skipping empty month: {year_month}")

        self.stdout.write(self.style.SUCCESS("Successfully split all data into monthly files."))