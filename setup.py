import os
import pathlib
import re

from setuptools import setup, find_packages

THIS_DIR = pathlib.Path(__file__).parent


def get_version() -> str:
    init_file = THIS_DIR / "src" / "prometheus_metrics_proto" / "__init__.py"
    version_re = re.compile(r".*__version__\s=\s+[\'\"](?P<version>.*?)[\'\"]")
    with open(init_file, "r", encoding="utf8") as init_fd:
        match = version_re.search(init_fd.read())
        if match:
            version = match.group("version")
        else:
            raise RuntimeError(f"Cannot find __version__ in {init_file}")
        return version


def get_long_description() -> str:
    readme_file = THIS_DIR / "README.md"
    with open(readme_file, encoding="utf8") as fd:
        readme = fd.read()
    return readme


def parse_requirements(filename):
    """ Load requirements from a pip requirements file """
    with open(filename, "r") as fd:
        lines = []
        for line in fd:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines


if __name__ == "__main__":

    setup(
        name="prometheus_metrics_proto",
        version=get_version(),
        author="Chris Laws",
        author_email="clawsicus@gmail.com",
        description="Prometheus binary format metrics data structures for Python client libraries",
        long_description=get_long_description(),
        license="MIT",
        keywords=["prometheus", "monitoring", "metrics"],
        url="https://github.com/claws/prometheus_metrics_proto",
        package_dir={"": "src"},
        packages=find_packages("src"),
        install_requires=parse_requirements("requirements.txt"),
        pyrobuf_modules="proto",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: System :: Monitoring",
        ],
    )
