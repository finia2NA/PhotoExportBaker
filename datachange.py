import pywintypes
import win32file
import win32con
import datetime


def changeFileCreationTime(fname, newtime):
  wintime = pywintypes.Time(newtime)
  winfile = win32file.CreateFile(
      fname, win32con.GENERIC_WRITE,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
      None, win32con.OPEN_EXISTING,
      win32con.FILE_ATTRIBUTE_NORMAL, None)

  win32file.SetFileTime(winfile, wintime, None, None)

  winfile.close()


changeFileCreationTime("thetestfile.rtf", 1434096560)
