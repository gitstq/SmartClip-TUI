"""
Test Content Classifier
测试内容分类器
"""

import pytest
from smartclip.classifier import ContentClassifier


class TestContentClassifier:
    """测试内容分类器"""

    def test_classify_url(self):
        content = "https://github.com/user/repo"
        type_name, tags = ContentClassifier.classify(content)
        assert type_name == "url"
        assert "url" in tags

    def test_classify_email(self):
        content = "user@example.com"
        type_name, tags = ContentClassifier.classify(content)
        assert type_name == "email"
        assert "email" in tags

    def test_classify_code(self):
        content = "def hello():\n    print('world')"
        type_name, tags = ContentClassifier.classify(content)
        assert type_name == "code"
        assert "code" in tags

    def test_classify_command(self):
        content = "git clone https://github.com/user/repo"
        type_name, tags = ContentClassifier.classify(content)
        assert type_name == "command"

    def test_classify_json(self):
        content = '{"key": "value", "num": 123}'
        type_name, tags = ContentClassifier.classify(content)
        assert type_name == "json"

    def test_classify_text(self):
        content = "This is a simple text"
        type_name, tags = ContentClassifier.classify(content)
        assert type_name == "text"

    def test_detect_python(self):
        content = "def hello():\n    return 'world'"
        lang = ContentClassifier._detect_code_language(content)
        assert lang == "python"

    def test_detect_javascript(self):
        content = "const x = () => console.log('hello');"
        lang = ContentClassifier._detect_code_language(content)
        assert lang == "javascript"

    def test_generate_summary(self):
        content = "First line\nSecond line\nThird line"
        summary = ContentClassifier.generate_summary(content)
        assert "First line" in summary
        assert "+2 lines" in summary

    def test_empty_content(self):
        type_name, tags = ContentClassifier.classify("")
        assert type_name == "empty"
