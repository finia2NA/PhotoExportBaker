import pywintypes
import win32file
import win32con
import datetime
import os
import json


def crawl(rootdir):
  pathlist = []
  for root, dirs, files in os.walk(rootdir):
    for fname in files:
      fpath = os.path.join(root, fname)
      pathlist.append(fpath)
  return pathlist


def getcorrectionDict(rootdir):
  numMetaFiles = 0
  numOkFiles = 0
  numBadFiles = 0
  numCreatedDates = 0
  numTakenDates = 0
  numMissmatches = 0

  allFiles = crawl(rootdir)

  jsons = [f for f in allFiles if f.endswith('.json')]
  photos = [f for f in allFiles if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg') or f.endswith(
      '.gif') or f.endswith('.bmp')]  # this horrible line of code is presented to you by github copilot

  correctionDict = {}  # format: filename -> date
  for jsonPath in jsons:
    if("metadata") in jsonPath:
      # these kinds of jsons are used for albums and are not useful for us
      numMetaFiles += 1
      continue

    data = None
    name = None

    try:
      data = json.load(open(jsonPath))
    except:
      print("Error loading json: " + jsonPath)
      numBadFiles += 1
      continue

    # First, get the file name
    try:
      fileNameFromJson = rootdir + "\\" + data['title']
      fileNameFromPath = jsonPath[:-5]
      if fileNameFromJson != fileNameFromPath:
        print("Warning: Filename mismatch between json and path: " +
              fileNameFromJson + " vs " + fileNameFromPath)
        numMissmatches += 1
      if fileNameFromJson not in photos and fileNameFromJson not in jsons:
        print("Warning: Neither " + fileNameFromJson +
              ", nor " + fileNameFromPath + " in photos ")
        numBadFiles += 1
        continue

      name = fileNameFromPath if fileNameFromPath in photos else fileNameFromJson
    except KeyError:
      print("Error: No title in json: " + jsonPath)
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
        print("Error: No date in json: " + jsonPath)
        continue
    numOkFiles += 1

  # print stats while we're at it
  print("Stats:")
  print("OK Files:           "+ str(numOkFiles))
  print("Bad Files:          "+ str(numBadFiles))
  print("Meta Files:         "+ str(numMetaFiles))
  print("Name Missmatches:   "+ str(numMissmatches))
  print("Created Dates Used: "+ str(numCreatedDates))
  print("Taken Dates Used:   "+ str(numTakenDates))


  return correctionDict


def changeFileCreationTime(fname, newtime):
  wintime = pywintypes.Time(newtime)
  winfile = win32file.CreateFile(
      fname, win32con.GENERIC_WRITE,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
      None, win32con.OPEN_EXISTING,
      win32con.FILE_ATTRIBUTE_NORMAL, None)

  win32file.SetFileTime(winfile, wintime, None, None)

  winfile.close()


def main():
  rootdir = os.getcwd() + "\\photos"
  correctionDict = getcorrectionDict(rootdir)
  for fname in correctionDict:
    changeFileCreationTime(fname, correctionDict[fname])


main()

# Test the building of the correction dict
# print(getcorrectionDict(os.getcwd() + "\\photos))

# Test crawling
# print(crawl(os.getcwd() + "\\photos))

# Test 3: changing file creation time
# changeFileCreationTime("testfile", 1434096560)
