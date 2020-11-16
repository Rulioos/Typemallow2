import os
import setuptools

with open('README.md') as file:
    long_description = file.read()

setuptools.setup(
    name="typemallow2",
    version="0.0.3",
    url="https://github.com/adenh93/typemallow",

    author="Jules Aubier",
    author_email="jules.aubier97@gmail.com",

    description="An elegant and automatic solution for generating/outputting Typescript interfaces and enums from your Marshmallow Schemas and enums classes."
                "Extension of Aden Harold works on typemallow.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['Marshmallow', 'Typescript', 'Python', 'Flask', 'Django'],

    packages=['typemallow2'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',

    install_requires=[
        'marshmallow>=2.0.0',
        'marshmallow_enum>=1.5'
    ])
