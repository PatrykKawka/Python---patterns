import time
import gc
import win32com.client as win32

FILE_PATH = r"C:\Sciezka\do\pliku.xlsx"

excel = win32.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
excel.AskToUpdateLinks = False

wb = None
try:
    wb = excel.Workbooks.Open(FILE_PATH)
    wb.RefreshAll()

    excel.CalculateUntilAsyncQueriesDone()

    wb.Save()
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
