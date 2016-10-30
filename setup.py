from setuptools import setup

with open("README.md", 'r') as f:
        long_description = f.read()

        setup(name='weather',
                    version='0.0.1',
                    description=u"Collect weather data from Raspberry pi",
                    long_description=long_description,
                    classifiers=[],
                    keywords='',
                    author=u"Jamie Tolan",
                    author_email='jamie.tolan@gmail.com',
                    url='https://github.com/jetolan/weather',
                    license='MIT',
                    packages=['Adafruit_Python_BME280', 'Adafruit_Python_MCP9808'],
                    package_dir={'Adafruit_Python_BME280': 'Adafruit_Python_BME280', 'Adafruit_Python_MCP9808':'Adafruit_Python_MCP9808'},
                    install_requires=['numpy', 'pandas']
                    )
