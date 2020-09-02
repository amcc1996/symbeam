format:
	black -l 92 symbeam

coverage:
	pytest --cov-report html --cov symbeam
	
clean:
	@rm -rf *.egg-info/
	@find . -name *__pycache__ -exec rm -rf {} +
	@echo Removed *.egg-info and __pycache__
