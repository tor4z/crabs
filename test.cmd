@set PYTHONPATH=%PYTHONPATH%;%cd%
@cd test
@python -m unittest discover --pattern=*.py -v
@cd ..