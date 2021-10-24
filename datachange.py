import pywintypes
import win32file
import win32con
import datetime
import os
import json

class FileDescriptor:
  def __init__(self, fname, fpath, froot):
    self.fname = fname
    self.froot = froot
    self.fpath = fpath
    

def crawl(rootdir):
  pathlist = []
  for root, dirs, files in os.walk(rootdir):
    for fname in files:
      fpath = os.path.join(root, fname)
      pathlist.append(FileDescriptor(fname, fpath, root))
  return pathlist


def getcorrectionDict(rootdir):
  numMetaFiles = 0
  numOkFiles = 0
  numBadFiles = 0
  numCreatedDates = 0
  numTakenDates = 0
  numMissmatches = 0

  allFiles = crawl(rootdir)
  allPaths = [f.fpath for f in allFiles]

  jsons = [f for f in allFiles if f.fname.endswith('.json')]
  # media = [f for f in allFiles if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith(
  #    '.gif') or f.endswith('.bmp') or f.endswith('.mp4') or f.endswith('.mov') or f.endswith('.avi') or f.endswith('.3gp')
  #    or f.endswith('.heic') or f.endswith('.mkv') or f.endswith('.m4v') or f.endswith('.webp')]

  correctionDict = {}  # format: filename -> date
  for jsonDescriptor in jsons:
    if("metadata") in jsonDescriptor.fname:
      # these kinds of jsons are used for albums and are not useful for us
      numMetaFiles += 1
      continue

    data = None
    name = None

    try:
      data = json.load(open(jsonDescriptor.fpath))
    except:
      print("Error loading json: " + jsonDescriptor.fpath)
      numBadFiles += 1
      continue

    # First, get the file name
    try:
      fileNameFromJson = jsonDescriptor.froot + "\\" + data['title']
      fileNameFromPath = jsonDescriptor.fpath[:-5]
      if fileNameFromJson != fileNameFromPath:
        print("Warning: Filename mismatch between json and path: " +
              fileNameFromJson + " vs " + fileNameFromPath)
        numMissmatches += 1
      if fileNameFromJson not in allPaths and fileNameFromJson not in allPaths:
        print("Warning: Neither " + fileNameFromJson +
              ", nor " + fileNameFromPath + " in photos ")
        numBadFiles += 1
        continue

      name = fileNameFromJson if fileNameFromJson in allFiles else fileNameFromPath
    except KeyError:
      print("Error: No title in json: " + jsonDescriptor)
      numBadFiles += 1
      continue

    # Then, get the date
    # preferrably, take takendate, but if that does not exist (eg for screenshots), use createdate
    # if that also does not exist we are f**ked
    try:
      takenDate = int(data['photoTakenTime']['timestamp'])
      correctionDict[name] = takenDate
      numTakenDates += 1
    except KeyError:
      try:
        createdDate = int(data['creationTime']['timestamp'])
        correctionDict[name] = createdDate
        numCreatedDates += 1
      except KeyError:
        print("Error: No date in json: " + jsonDescriptor)
        continue
    numOkFiles += 1

  # print stats while we're at it
  print("Stats:")
  print("OK Files:           " + str(numOkFiles))
  print("Bad Files:          " + str(numBadFiles))
  print("Meta Files:         " + str(numMetaFiles))
  print("Name Missmatches:   " + str(numMissmatches))
  print("Created Dates Used: " + str(numCreatedDates))
  print("Taken Dates Used:   " + str(numTakenDates))

  return correctionDict


def changeFileTimes(fname, newtime, changeAll=True):
  wintime = pywintypes.Time(newtime)
  winfile = win32file.CreateFile(
      fname, win32con.GENERIC_WRITE,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
      None, win32con.OPEN_EXISTING,
      win32con.FILE_ATTRIBUTE_NORMAL, None)

  if changeAll:
    win32file.SetFileTime(winfile, wintime, wintime, wintime)
  else:
    win32file.SetFileTime(winfile, wintime, None, None)

  winfile.close()


def main():
  rootdir = os.getcwd() + "\\photos"
  correctionDict = getcorrectionDict(rootdir)
  for fname in correctionDict:
    changeFileTimes(fname, correctionDict[fname])


if __name__ == "__main__":
  main()

# Test the building of the correction dict
# print(getcorrectionDict(os.getcwd() + "\\photos))

# Test crawling
# print(crawl(os.getcwd() + "\\photos))

# Test 3: changing file creation time
# changeFileCreationTime("testfile", 1434096560)
