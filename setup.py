# ! important
# see https://stackoverflow.com/a/27868004/1497139
import pathlib
from setuptools import setup
from collections import OrderedDict
from jpwidgets.version import Version
here = pathlib.Path(__file__).parent.resolve()
readme= (here/"README.md").read_text()
requirements = (here / 'requirements.txt').read_text().split("\n")

setup(name=Version.name,
    version=Version.version,
    description=Version.description,
    long_description=readme,
    long_description_content_type='text/markdown',
    url=f'http://wiki.bitplan.com/index.php/{Version.name}',
    download_url=f'https://github.com/WolfgangFahl/{Version.name}',
    author='Wolfgang Fahl',
    author_email='wf@bitplan.com',
    license='Apache',
    project_urls=OrderedDict(
        (
            ("Code", f"https://github.com/WolfgangFahl/{Version.name}"),
            ("Issue tracker", f"https://github.com/WolfgangFahl/{Version.name}/issues"),
        )
    ),
    classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
      ],
    packages=['jpwidgets','jpdemo'],
    install_requires=requirements,
    zip_safe=False)
