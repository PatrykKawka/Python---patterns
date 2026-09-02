import time
import gc
import win32com.client as win32

FILE_PATH = r"C:\Sciezka\do\pliku.xlsx"

excel = win32.DispatchEx("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
excel.AskToUpdateLinks = False

wb = excel.Workbooks.Open(FILE_PATH)
wb.RefreshAll()
time.sleep(60)

excel.CalculateUntilAsyncQueriesDonce()


wb.Save()
wb.Close()
excel.Quit()

time.sleep(10)

del wb
del excel
gc.collect()
