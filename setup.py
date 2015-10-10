from setuptools import find_packages
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='sabertooth',
    version='0.3.2',
    description="An OpenSubtitles Client",
    long_description=read_md('README.md'),
    author='Walid Saad',
    author_email='walid.sa3d@gmail.com',
    url='https://github.com/walidsa3d/sabertooth',
    license="MIT",
    keywords="cli subtitles opensuhbtitles",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["sabertooth=sabertooth.cli:main"]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ]
)
