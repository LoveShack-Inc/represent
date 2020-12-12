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
    url="https://github.com/LoveShack-Inc/represent",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[
        "requests",
        "pdfplumber",
        "certifi",
        "beautifulsoup4",
        "cherrypy",
        "pytest",
        "pandas"
    ],
    entry_points = {
        'console_scripts': [
            'repp=rep.main:main', 
            'repp-crawl=rep.crawlers.CtGovCrawler.main',
            'repp-serve=rep.service:main'
        ],
    }
)
