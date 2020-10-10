import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rep",
    version="0.0.1",
    author="LoveShack Inc",
    description="Are you represented?",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dalton-b/am-i-represented",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[
        "requests",
        "PyPDF2",
        "certifi",
        "beautifulsoup4"
    ],
    entry_points = {
        'console_scripts': ['repp=rep.main:main', 'crawl=rep.crawlers.CtGovCrawler.main'],
    }
)
