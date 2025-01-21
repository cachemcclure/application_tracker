from setuptools import find_packages, setup


package_version = "0.0.1"

requirements = [
    "PyQt6==6.8.0",
    "pyqtgraph==0.13.7"
]

dev_requirements = [
    "black>=22.3.0"
]

setup(
    name="application-tracker",
    python_requires=">=3.11",
    version=package_version,
    description="A basic interactive job application tracker.",
    author="Cache McClure",
    author_email="cache.mcclure@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
)
