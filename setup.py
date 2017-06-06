from distutils.core import setup

setup(name='Exipe',
      version='1.0',
      description='Information Retrieval API for Presentation Documents',
      author='Yanis Ouakrim',
      author_email='yanis.ouakrim@etu.univ-nantes.fr',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['exipe', 'exipe.datatypes'],
      install_requires=['python-pptx', 'nltk', 'zipfile', 'jsonpickle', 'json']
      )