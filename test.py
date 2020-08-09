import pyautogui
from datetime import date, datetime
ss = pyautogui.screenshot()
path = str(date.today()) + "_" +str(datetime.now().strftime("%H_%M_%S")) +".png"
ss.save(path)
