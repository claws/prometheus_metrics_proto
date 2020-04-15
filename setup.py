
import os
import re

from setuptools import setup, find_packages

regexp = re.compile(r'.*__version__ = [\'\"](.*?)[\'\"]', re.S)


init_file = os.path.join(
    os.path.dirname(__file__), 'src', 'prometheus_metrics_proto', '__init__.py')
with open(init_file, 'r') as f:
    module_content = f.read()
    match = regexp.match(module_content)
    if match:
        version = match.group(1)
    else:
        raise RuntimeError(
            'Cannot find __version__ in {}'.format(init_file))

with open('README.rst', 'r') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    requirements = [line for line in f.read().split('\n') if len(line.strip())]



if __name__ == "__main__":

    setup(
        name="prometheus_metrics_proto",
        version=version,
        author="Chris Laws",
        author_email="clawsicus@gmail.com",
        description="Prometheus binary format metrics data structures for Python client libraries",
        long_description=readme,
        license="MIT",
        keywords=["prometheus", "monitoring", "metrics"],
        url="https://github.com/claws/prometheus_metrics_proto",
        package_dir={'': 'src'},
        packages=find_packages('src'),
        install_requires=requirements,
        pyrobuf_modules="proto",
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.6",
            "Topic :: System :: Monitoring"])
