from distutils.core import setup

setup(name='Exide',
      version='3.9.4',
      description='Information Retrieval API for Presentation Documents',
      author='Yanis Ouakrim',
      author_email='yanis.ouakrim[at]etu.univ-nantes.fr',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['exide', 'exide.datatypes', 'exide.odp_element_parsers', 'exide.pptx_element_parsers', 'exide.dict'],
      package_data={'': ['*.txt']},
      include_package_data=True,
      install_requires=['python-pptx', 'nltk', 'jsonpickle']
      )
