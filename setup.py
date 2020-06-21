from setuptools import setup, find_packages

setup(
    name="random_char_image",
    version="0.0.0",
    description="TODO",
    author="Xinyuan Yao",
    author_email="yao.ntno@google.com",
    license="TODO",
    packages=find_packages(),
    package_data={"random_char_image": ["py.typed"],},
    install_requires=["Pillow", "numpy",],
    extras_require={"dev": ["mypy", "pytest", "black",]},
)
