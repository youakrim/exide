# exipe2

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

Note : slide types can be added by editing the datatypes/types file.

For now the API works only with Office Open XML Presentation files (PPTX) and OpendDocument Presentation files (ODP). It uses python-pptx and NLTK librairies.
Documentation is not yet written.
