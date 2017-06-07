# exipe

Exipe is a Python API for information extraction from presentation documents.

The API is currently in developement and bugs are likely to occur.

### Implemented features : 
* Slide title extraction
* Slide body text extraction
* Named-entities recognition (unaccurate)
* Emphasized text recognition
* URLs recognition
* Structure detection and outline generation
* Recognition of the following silde types : 
  * Introduction 
  * Conclusion
  * Definition 
  * Example
  * Table of contents
  * References
  * Section header
 
### Supported file types
* Office Open XML Presentations (PPTX)
* OpenDocument Presentations (ODP)
* LaTeX beamer Presentations

Note : slide types can be added by editing the datatypes/types file.
### Install exipe
cd to the root of the exipe package directory and then : 
```bash
sudo pip install .
```
