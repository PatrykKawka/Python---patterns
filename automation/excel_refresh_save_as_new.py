import time
import gc
from datetime import datetime
from pathlib import Path
import win32com.client as win32

FILE_PATH = r"C:\Sciezka\do\pliku.xlsx"
OUTPUT_DIR = None

source_path = Path(FILE_PATH)
target_dir = Path(OUTPUT_DIR) if OUTPUT_DIR else source_path.parent
refresh_stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
new_path = target_dir / f"{source_path.stem}_odswiezono_{refresh_stamp}{source_path.suffix}"

excel = win32.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
excel.AskToUpdateLinks = False

wb = None
try:
    wb = excel.Workbooks.Open(str(source_path))
    wb.RefreshAll()

    excel.CalculateUntilAsyncQueriesDone()

    wb.SaveAs(str(new_path))
    wb.Close()
    wb = None

finally:
    if wb is not None:
        try:
            wb.Close(SaveChanges=False)
        except Exception as e:
            print(f"Ostrzeżenie: {e}")

    if excel is not None:
        try:
            excel.Quit()
        except Exception as e:
            print(f"Ostrzeżenie: {e}")

    del wb
    del excel

    gc.collect()
