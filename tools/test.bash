#!/usr/bin/env bash

cd ../dist
RELEASE_ARCHIVE=`ls prometheus_metrics_proto-*.tar.gz`

if [ -z "$RELEASE_ARCHIVE" ]; then
  echo "No release archive found. Expected prometheus_metrics_proto-YY.MM.MICRO.tar.gz"
  exit
fi

RELEASE_DIR=`echo $RELEASE_ARCHIVE | sed -e "s/\.tar\.gz//g"`

echo "Release archive: $RELEASE_ARCHIVE"
echo "Release directory: $RELEASE_DIR"

echo "Removing any old artefacts"
rm -rf $RELEASE_DIR
rm -rf test_venv

echo "Creating test virtual environment"
python -m venv test_venv

echo "Entering test virtual environment"
source test_venv/bin/activate

echo "Upgrading pip"
pip install pip --upgrade

echo "Installing $RELEASE_ARCHIVE"
tar xf $RELEASE_ARCHIVE
cd $RELEASE_DIR
pip install .

echo "Running tests"
make test
cd ..

echo "Exiting test virtual environment"
deactivate
