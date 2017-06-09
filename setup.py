from distutils.core import setup

setup(name='Exipe',
      version='3.8.5',
      description='Information Retrieval API for Presentation Documents',
      author='Yanis Ouakrim',
      author_email='yanis.ouakrim[at]etu.univ-nantes.fr',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['exipe', 'exipe.datatypes', 'exipe.odp_element_parsers', 'exipe.pptx_element_parsers', 'exipe.dict'],
      package_data={'': ['*.txt']},
      include_package_data=True,
      install_requires=['python-pptx', 'nltk', 'jsonpickle']
      )
