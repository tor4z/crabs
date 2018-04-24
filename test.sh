#!/usr/bin/env bash
export PYTHONPATH="$(pwd)"
cd test
python -m unittest discover -v --pattern=*.py
cd ..