# PhotoExportBaker
When exporting your photo collection from Google Photos, you'll realize that the photos do not actually have their creation and modification times as part of their file metadata. Instead, this data is contained in seperate .json sidecar files.

This can be very annoying when importing the photo to another service, such as Synology Photos.
What happens is that all images that do not have their "photoTakenTime" as part of their jpg metadata get dumped at the location of their file metadata, leading to a giant, unorganized mess.

This program bakes the timestamps from the .jsons into the file metadata of the photos, leading to them being correctly placed when importing to another service.

# Usage and Restrictions
To use this program, install the requirements:
```pip install -r requirements.txt```
, then place your google photos export in a folder names "photos" and run the program.

Sadly, the program only works on Windows right now because of the use of a Windows-specific library.