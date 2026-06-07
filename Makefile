.PHONY: install test lint format clean build run help

help:
	@echo "SmartClip-TUI Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install     Install dependencies"
	@echo "  test        Run tests"
	@echo "  lint        Run linter"
	@echo "  format      Format code"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build package"
	@echo "  run         Run TUI application"
	@echo "  setup       Setup development environment"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --tb=short

lint:
	flake8 smartclip/ tests/
	black --check smartclip/ tests/

format:
	black smartclip/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

run:
	python -m smartclip tui

setup: install dev
	@echo "✅ Development environment setup complete"
