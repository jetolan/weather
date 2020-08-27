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
          install_requires=['numpy', 'pandas', 'RPI.GPIO', 'adafruit-blinka',
                            'adafruit_platformdetect',
                            'adafruit-circuitpython-ina219',
                            'adafruit-circuitpython-bme280']
          )
