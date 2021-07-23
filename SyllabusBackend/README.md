# Syllabus Builder (Backend)

## Description
Build a syllabus!

## Dependencies
* BeautifulSoup4
* DocxCompose
* PyPandoc
* PyPDF2
* PythonDocx
* Requests

## File Structure
### main.py
This just runs everything.

### syllabus.py
Contains the `DOCXWriter()` class. This is the main meat of the program, and this is what actually builds and generates the .docx.

### parsepdf.py
Goes to the Registrar's website and downloads the academic calendar for a given semester, then parses it into useable form.

### ~~scrape_oei.py~~
~~Simply retrieves the article tag from the OEI's required language webpage.~~

### scheduler.py
Handles all of the meeting table creation. Can work standalone or in tandem with syllabus.py.
