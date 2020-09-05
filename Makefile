format:
	black -l 92 symbeam

coverage:
	pytest --cov-report html --cov symbeam
	
clean:
	@rm -rf *.egg-info/
	@if [ -d "htmlcov" ]; then rm -rf htmlcov; echo Removed hmltcov; fi
	@find . -name *__pycache__ -exec rm -rf {} +
	@echo Removed *.egg-info and __pycache__
