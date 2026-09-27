from pathlib import Path
import pandas as pd #pobieranie wcześniej przy pbróbce df

values_do_split_by = set(df['kolumna']) #unikalne wartości z kolumny

folder = Path.cwd()
output_dir = folder/"Output"
output_dir.mkdir(parents=True, exist_ok=True)


for value in values_do_split_by:
    df_file = df[df['kolumna'] == value]
    df_file_path = output_dir / f"{value}.xlsx"

    df_file.to_excel(df_file_path, index=False)
    print(f'Zapisano plik {df_file_path.stem} w {output_dir}')

print(f'Zapisano wszystkie pliki, łącznie {len(values_do_split_by)}')
