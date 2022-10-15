from setuptools import find_packages, setup

def get_version() -> str:
    with open("VERSION", "r") as file:
        return file.read().strip()


setup(
    name="Spotify_Recommender",
    version=get_version(),
    author="ebarrios95",
    description="App to create a playlist of a user defined number of songs",
    url="https://github.com/ebarrios95/SpotifyRecommender",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pylint==2.15.2",
        "spotipy==2.19.0",
        "pandas==1.5.0",
        "kivymd==1.1.1",
        "build==0.8.0"
    ]
    classifiers=[
        "Prgramming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ])