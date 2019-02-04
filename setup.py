from setuptools import setup

LONG_DESCRIPTION = open('README.md').read()

setup(name='aws_lambda_decorators',
      version='0.1',
      description='A set of python decorators to simplify aws python lambda development',
      long_description=LONG_DESCRIPTION,
      url='',
      author='',
      author_email='',
      license='MIT',
      classifiers=['Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.6'
                   ],
      keywords='aws lambda decorator',
      packages=['aws_lambda_decorators'],
      zip_safe=False
      )
