from setuptools import setup

setup(name='pollingclient',
      version='1.0',
      description='UK Polling Client',
      author='NicksTricks',
      author_email='nick@nickaltmann.net',
      packages=['pollingclient'],
      install_requires=['pandas>=0.18.0',
                        ],
      )
