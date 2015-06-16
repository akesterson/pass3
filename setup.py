from distutils.core import setup
import pass3.version
import os
import sys

long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.rst'
    )
).read()

if __name__ == "__main__":
    setup(
        name="pass3",
        url="https://www.github.com/akesterson/pass3-python",
        version=pass3.version.VERSION,
        description="Filesystem-like pathing and searching for dictionaries",
        long_description=long_description,
        author=("Andrew Kesterson"),
        author_email="andrew@aklabs.net",
        license="MIT",
        install_requires=[],
        scripts=[
            'scripts/pass3'
            ],
        packages=["pass3"],
        data_files=[],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Console',
            'Environment :: MacOS X',
            'Environment :: X11 Applications',
            'Environment :: Win32',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Security',
        ],
    )

