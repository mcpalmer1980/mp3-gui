# MP3 GUI - Tools for working with MP3 files

The following Tools are available by pressing their buttons at the top of the main
window. Tools will output their status into the text box at the center and you
can copy the text with the button at the bottom.

**Sync to Dest** - FUCK Copy missing MP3s from source folder to chosen destination  
**Clean Dest** - Remove any files from destination folder if missing in source folder  
**Verify Filenames** - Compare filenames to MP3 tags and detect mangled filenames  
**Show non-MP3s** - Show or delete non-MP3 files in source folder  
**Fix Playlist** - Normalize playlist to use relative paths and remove extra lines  
**Browser** - Button for testing my custom file browser  
**Artists** - Display all artists in source folder and edit mislabeled artist tags  
**Albums** - Display all albums in source folder and edit mislabeled albums tags  
**Genres** - Display all genres in source folder and edit mislabeled genres tags  
**Tag Editor** - Show, filter, and edit the tags for all MP3s in source folder  
**Change Theme** - Change GUI colors and font size  

## Sync to Dest
Copy MP3s files missing from the source folder to the chosen destination

### Functions:  
- Source - Select, type, or browse for a source folder from the history dropdown
- Dest - Select, type, or browse for a destination folder from the history dropdown
- Swap - Quickly swap the source and destinatation folders
- Scan - Compare the source and desintation folders and display the results
- Copy - Copy the files displayed in the result window to the destination folder

### Options:
- Missing - Show/copy MP3 files missing in the destination folder
- Different - Show/copy MP3 files different in the destination folder
- Same - Show/copy MP3 files that are the same in the destination folder
- Extra - Show/copy non-MP3 files that are in the destination folder
- Clear - Change the album tag to the artist name in the destination folder copy
- CRC - Use the CRC when comparing files for differences (SLOW)

## Clean Dest
Remove any files from the destination folder that are missing in source folder

### Functions:  
- Source - Select, type, or browse for a source folder from the history dropdown
- Dest - Select, type, or browse for a destination folder from the history dropdown
- Swap - Quickly swap the source and destinatation folders
- List - Click listed files to remove them from the list (so not to delete them)
- Remove - Remove files from destination folder that are missing in the source

### Options:
- MP3s - Include MP3 files when viewing/removing files
- Other - Include non-MP3 files when viewing/removing files

## Verify Filenames
Compare filenames to MP3 tags and detect mangled filenames

### Functions:
- Source - Select, type, or browse for a source folder from the history dropdown
- Match - A match string for comparing filenames to MP3 tags, detailed below
- Scan - Scan for filenames with extra spaces or other common irregularities
- Compare - Scan for and display both the filename with the expected filename
- List - Click a listed file to edit its tags

### Options:
- Ignore Folders - Compare filenames only, ignoring any subfolders

### Match Strings:
Match strings can include any text seperating the {title}, {artist}, {album}, or {genre} tags.  
  
Here are a few examples:  
**{artist} - {title}** - "Michael Jackson - Beat It.mp3"  
**{artist}/{album}/{title}** - "Metallica/Black/Enter Sandman.mp3"  

## Show non-MP3s
Show or delete non-MP3 files in source folder

### Functions:
- Source - Select, type, or browse for a source folder from the history dropdown
- Reset - Update the list to add files that were filtered out
- Remove - Delete from the source folder any files currently shown in the list
- List - Remove files from the list by clicking them

### Options:
- Filter Same Folder - Filter all files from the same folder when you click one
- Filter Same Extentions - Filter all files with same extension when you click one

## Fix Playlist
Normalize playlist to use relative paths and remove extra lines

### Functions
- Playlist - Type or browse for a playlist to edit
- Strip - The string to strip from the begining of the filenames
- Prefix - Prefix to add to the beginning of the filenames
- List - Click files to remove them from the playlist
- Show - Show the converted output instead of the original filename
- Reset - Show the original filename instead of the converted output
- Save - Save the playlist with the new converted output

### Options
- Remove Metadata - Remove descriptive lines (begining with #) from the playlist
- Remove Missing - Remove invalid entries that link to missing files 
- Remove Clicked - Remove entries when you click them in the listbox

## Artists  
Display all artists in source folder, edit artist tags, and export artist playlists

### Functions
- Source - Select, type, or browse for a source folder from the history dropdown
- Export Subfolder - Enter name for subfolder to export playlists into
- List - Click a listed artist to edit the artist tag for each song by them
- Copy - Copy displayed artist list into the clipboard
- Make Playlists - Export playlist for each artist currently displayed

### Options
- Sort by Count - Sort artists by song count instead of alphabetically
- Extra Details - Display ablums from each artist
- Unfold Details - Display each album on its own line of text 
- Minimum Count - Only artists with at least this number of songs will be shown
- Play on Click - Play songs by an artist when you click instead of editing

## Albums  
Display all albums in source folder, edit album tags, and export album playlists

### Functions
- Source - Select, type, or browse for a source folder from the history dropdown
- Export Subfolder - Enter name for subfolder to export playlists into
- List - Click a listed album to edit the album tag for each song on it
- Copy - Copy displayed album list into the clipboard
- Make Playlists - Export playlist for each ablum currently displayed

### Options
- Sort by Count - Sort ablums by song count instead of alphabetically
- Extra Details - Display songs from each album
- Unfold Details - Display each song on its own line of text 
- Minimum Count - Only ablums with at least this number of songs will be shown

## Genres
Display all genres in source folder, edit genre tags, and export genre playlists

### Functions
- Source - Select, type, or browse for a source folder from the history dropdown
- Export Subfolder - Type name for subfolder to export playlists into
- List - Click a listed genre to edit the genre tag for each song in them
- Copy - Copy displayed genre list into the clipboard
- Make Playlists - Export playlist for each genre currently displayed

### Options
- Sort by Count - Sort genre by song count instead of alphabetically
- Extra Details - Display artists in each genre
- Unfold Details - Display each artist on its own line of text 
- Minimum Count - Only genres with at least this number of songs will be shown

## Tag Editor  
Show, filter, and edit the tags for all MP3s in source folder

### Functions
- Source - Select, type, or browse for a source folder from the history dropdown
- Scan - Scan the source folder and display tags for each MP3 found
- Filter - Enter text to filter from the song list
- Key - Choose which tag to search for filter text or any to search them all
- Include - Filter songs that include the given filter text
- Exclude - Filter songs that do not include the given filter text
- Reset - Reset all filters and display the entire song list
- Table - Click on a selected song to edit its tags (double click)
- Play Song - Play the currently selected song(s) in your default MP3 player
- Multi Edit - Edit tags for multiple selected files at once

### Options
- Case Sensitive - Only match filter text if the case matches exactly
- Play Songs - Play songs instead of editing tags when you click them
