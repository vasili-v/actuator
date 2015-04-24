from setuptools import setup, find_packages

setup(
    name = "Actuator",
    version = "0.1",
    packages = find_packages(exclude=['test']),
    description = "Actuator library simplifies creation of python scripts",
    url = "https://github.com/vasili-v/actuator",
    author = "Vasili Vasilyeu",
    author_email = "vasili.v@tut.by",
    license = "MIT",
    long_description = "Actuator library allows to create python script with " \
                       "sophisticated argument processing",
    platforms = ["Darwin", "Linux"],
    test_suite = "test.all"
)
