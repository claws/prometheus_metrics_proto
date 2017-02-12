

from pip.req import parse_requirements
from pip.download import PipSession
from setuptools import setup, find_packages


requires = [str(ir.req) for ir in parse_requirements("requirements.txt", session=PipSession())]


if __name__ == "__main__":

    setup(
        name="prometheus_metrics_proto",
        version="17.02.01",
        author="Chris Laws",
        author_email="clawsicus@gmail.com",
        description="Prometheus binary format metrics data structures for Python client libraries",
        long_description="",
        license="MIT",
        keywords=["prometheus", "monitoring", "metrics"],
        url="https://github.com/claws/prometheus_metrics_proto",
        packages=find_packages(),
        install_requires=requires,
        pyrobuf_modules="proto",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Topic :: System :: Monitoring"])
