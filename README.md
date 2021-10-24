# PhotoExportBaker
When exporting your photo collection from Google Photos, you'll realize that the photos do not actually have their Creation and Modification times as part of their Metadata. Instead, this data is contained in a .json sidecar file.

This can be very annoying when importing the photo to another service, such as Synology Photos.
What happens is that all images that do not have their "photoTakenTime" as part of their jpg metadata get dumped at the location of their file metadata, leading to a giant, unorganized mess

This program bakes the created data from the jsons into the file metadata of the photos, leading to them being correctly placed when importing to another service.