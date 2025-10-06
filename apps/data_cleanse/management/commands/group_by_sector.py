import os
from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd

class Command(BaseCommand):
    help = "Groups monthly data files by 'GICs Sector' and saves them into new directories."

    def handle(self, *args, **options):
        # 1. 입력 폴더와 최상위 출력 폴더 경로 설정
        input_dir = Path("data/data_monthly/")
        output_dir = Path("data/sector_monthly/")

        if not input_dir.exists():
            self.stderr.write(self.style.ERROR(f"Input directory not found: {input_dir}"))
            self.stderr.write("Please run 'python manage.py data_monthly' first.")
            return

        # 최상위 출력 폴더 생성
        output_dir.mkdir(parents=True, exist_ok=True)
        self.stdout.write(f"Output will be saved in '{output_dir}'")

        # 2. 입력 폴더 안에 있는 모든 Parquet 파일을 순회
        monthly_files = sorted(list(input_dir.glob("merged_final_*.parquet")))
        if not monthly_files:
            self.stderr.write(self.style.ERROR(f"No monthly Parquet files found in {input_dir}"))
            return
            
        total_files = len(monthly_files)
        self.stdout.write(f"Found {total_files} monthly files to process...")

        for i, file_path in enumerate(monthly_files, 1):
            self.stdout.write(f"\n({i}/{total_files}) Processing {file_path.name}...")
            df = pd.read_parquet(file_path)

            # 3. 'GICS Sector' 컬럼이 있는지 확인 (대소문자 수정)
            sector_column = 'GICS Sector' # 컬럼 이름을 실제 데이터에 맞게 수정했습니다.
            if sector_column not in df.columns:
                self.stderr.write(self.style.WARNING(f"'{sector_column}' column not found in {file_path.name}. Skipping this file."))
                continue

            # 4. 'GICS Sector'를 기준으로 데이터 그룹화
            grouped_by_sector = df.groupby(sector_column)

            # 5. 월별로 하위 폴더 생성 (예: data/sector_monthly/2015-01/)
            month_str = file_path.stem.replace("merged_final_", "")
            monthly_output_dir = output_dir / month_str
            monthly_output_dir.mkdir(exist_ok=True)

            # 6. 각 섹터 그룹을 별도의 Parquet 파일로 저장
            for sector_name, sector_df in grouped_by_sector:
                # 파일 이름으로 사용하기 어려운 문자를 언더스코어(_)로 변경
                safe_sector_name = "".join(c if c.isalnum() else '_' for c in sector_name)
                output_filename = f"{safe_sector_name}.parquet"
                output_path = monthly_output_dir / output_filename

                if not sector_df.empty:
                    self.stdout.write(f"  -> Saving {sector_name} sector to {output_path}")
                    sector_df.to_parquet(output_path, index=False)

        self.stdout.write(self.style.SUCCESS("\nSuccessfully grouped all monthly data by sector."))