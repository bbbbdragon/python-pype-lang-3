from setuptools import setup, find_packages

#with open("README.md", "r") as fh:
#    LONG_DESCRIPTION=fh.read()

setup(name='python-pype-lang-3',
      version='3.0.27',
      description='Version 3 of pype, a Python-integrated functional programming language - Provides easy-to-use pseudo-macros for common functional programming tasks such as maps, reduces, filters, conditionals, dictionary manipulations, and list manipulations..',
      #long_description_content_type="text/markdown",
      #long_description=LONG_DESCRIPTION,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
      ],
      keywords='functional programming map reduce filter lambda conditional',
      url='https://github.com/bbbbdragon/python-pype-lang-3.git',
      author='Bennett Charles Bullock',
      author_email='bennettbullock36@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy',
          # 'numba',
          'colorama',
          'astpretty',
          'mmh3',
          'requests',
          'flask',
          'twine',
          'python-dateutil',
      ],
      include_package_data=True,
      zip_safe=False)
