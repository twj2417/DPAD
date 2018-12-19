from setuptools import setup, find_packages

setup(name='dpad',
      version='0.0.1',
      description='Processing data from actual system',
      url='https://github.com/twj2417/DPAD',
      author='Weijie Tao',
      author_email='twj2417@gmail.com',
      license='Apache',
      packages=find_packages('src/python'),
      package_dir={'': 'src/python'},
      install_requires=[
          'doufo==0.0.4',
          'jfs==0.1.3',
          'scipy',
          'matplotlib',
          'typing',
          'h5py',
          'click',
          'pathlib',
          'numpy',
      ],
      zip_safe=False)