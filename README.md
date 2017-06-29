# exide

Exide is a Python API for information extraction from presentation documents.

The API is currently in developement and bugs are likely to occur.

### Install exide
Download the repository, cd to the root of the exide package directory and then type the following : 
```bash
sudo su
pip install .
python
import nltk
nltk.download("all")
```
then press enter. 
Exide is now installed on your system.

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

### Supported file types
* Office Open XML Presentations (PPTX)
* OpenDocument Presentations (ODP)
* LaTeX beamer Presentations

### Simple example
The following code show you how to print the outline string of the file my_presentation.pptx.
```python
from exide.parse import parse
exide_presentation = parse("my_folder/my_presentation.pptx")
print(exide_presentation.outline)
```

