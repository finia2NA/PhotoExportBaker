# PhotoExportBaker
When exporting your photo collection from Google Photos, you'll realize that the photos do not actually have their "Created Date" as part of their Metadata. Instead, this data is contained in a .json sidecar file.

This can be very annoying when importing the photo to another service, such as Synology Photos.

This program bakes the created data into the photos, thus solving this problem.