from setuptools import find_packages
from setuptools import setup

setup(
    name='sabertooth',
    version='0.2.0',
    description="An OpenSubtitles Client",
    long_description=open('README.md').read(),
    author='Walid Saad',
    author_email='walid.sa3d@gmail.com',
    url='https://github.com/walidsa3d/sabertooth',
    license="MIT",
    keywords="cli subtitles opensuhbtitles",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["sabertooth=sabertooth.cli:main"]},
    classifiers=[
        'Development Status :: 4  - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities'
    ]
)
