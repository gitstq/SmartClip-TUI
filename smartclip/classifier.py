"""
Smart Content Classifier
智能内容分类器 - 自动识别剪贴板内容类型
"""

import re
from typing import List, Tuple


class ContentClassifier:
    """内容分类器"""

    # 正则表达式模式
    PATTERNS = {
        "url": re.compile(
            r'^https?://[^\s<>"{}|\\^`\[\]]+$',
            re.IGNORECASE
        ),
        "email": re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        ),
        "ip_address": re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        ),
        "command": re.compile(
            r'^(?:git|npm|pip|docker|kubectl|curl|wget|ssh|cd|ls|cat|'
            r'mkdir|rm|cp|mv|chmod|chown|sudo|apt|yum|brew|make|cargo|'
            r'go|python|node|yarn|pnpm)\s+',
            re.IGNORECASE
        ),
        "code_block": re.compile(
            r'^(?:def |class |function |const |let |var |import |from |'
            r'#include |using namespace |package |public class |'
            r'interface |type |struct |enum |async |await |=> |\{|\})',
            re.MULTILINE
        ),
        "json": re.compile(
            r'^\s*[\{\[]'
        ),
        "path": re.compile(
            r'^(?:/|[A-Za-z]:\\|~\/|\.\/|\.\.\/)'
        ),
    }

    @classmethod
    def classify(cls, content: str) -> Tuple[str, List[str]]:
        """
        分类内容类型
        返回: (主类型, [标签列表])
        """
        content = content.strip()
        if not content:
            return "empty", []

        lines = content.split('\n')
        first_line = lines[0].strip()

        # 检查各类型
        checks = [
            ("url", cls.PATTERNS["url"].match(first_line)),
            ("email", cls.PATTERNS["email"].match(first_line)),
            ("ip_address", cls.PATTERNS["ip_address"].match(first_line)),
            ("command", cls.PATTERNS["command"].match(first_line)),
        ]

        for type_name, matched in checks:
            if matched:
                tags = cls._extract_tags(content, type_name)
                return type_name, tags

        # 检查代码
        if cls._is_code(content):
            code_type = cls._detect_code_language(content)
            tags = ["code", code_type] if code_type else ["code"]
            return "code", tags

        # 检查JSON
        if cls.PATTERNS["json"].match(first_line):
            try:
                import json
                json.loads(content)
                return "json", ["data", "json"]
            except:
                pass

        # 检查路径
        if cls.PATTERNS["path"].match(first_line):
            return "path", ["file", "path"]

        # 检查密码/密钥
        if cls._is_password_or_key(content):
            return "password", ["sensitive", "secret"]

        # 默认文本
        return "text", cls._extract_tags(content, "text")

    @classmethod
    def _is_code(cls, content: str) -> bool:
        """判断是否为代码"""
        code_indicators = [
            r'\b(def|class|function|const|let|var|import|from|return|if|else|for|while)\b',
            r'[\{\}\(\);=+\-*/<>!&|]',
            r'^(\s{4}|\t)',  # 缩进
            r'#!/',  # Shebang
        ]

        score = 0
        for pattern in code_indicators:
            if re.search(pattern, content, re.MULTILINE):
                score += 1

        # 多行且有缩进，更可能是代码
        lines = content.split('\n')
        if len(lines) > 1:
            indented = sum(1 for line in lines if line.startswith(' ') or line.startswith('\t'))
            if indented / len(lines) > 0.3:
                score += 2

        return score >= 2

    @classmethod
    def _detect_code_language(cls, content: str) -> str:
        """检测代码语言"""
        indicators = {
            "python": [r'^\s*def\s+', r'^\s*class\s+', r'import\s+\w+', r'print\(', r'__init__'],
            "javascript": [r'const\s+', r'let\s+', r'var\s+', r'=>', r'console\.log'],
            "typescript": [r'interface\s+', r'type\s+', r':\s*(string|number|boolean)'],
            "go": [r'^package\s+', r'func\s+', r'fmt\.'],
            "rust": [r'^fn\s+', r'let\s+mut', r'println!'],
            "bash": [r'^#!/bin/bash', r'^#!/bin/sh', r'echo\s+'],
            "sql": [r'^SELECT\s+', r'^INSERT\s+', r'^UPDATE\s+', r'^DELETE\s+'],
            "html": [r'<\w+>', r'</\w+>', r'<!DOCTYPE'],
            "css": [r'^\.[a-zA-Z]', r'^#\w+\s*\{', r'@media'],
            "java": [r'^public\s+class', r'System\.out\.println'],
            "cpp": [r'#include', r'std::', r'int\s+main\s*\('],
        }

        scores = {lang: 0 for lang in indicators}
        for lang, patterns in indicators.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                    scores[lang] += 1

        if scores:
            best = max(scores, key=scores.get)
            if scores[best] > 0:
                return best
        return ""

    @classmethod
    def _is_password_or_key(cls, content: str) -> bool:
        """判断是否为密码或密钥"""
        patterns = [
            r'^(?:password|passwd|pwd|secret|token|key|api[_-]?key)\s*[=:]\s*\S+',
            r'^[A-Za-z0-9+/]{32,}={0,2}$',  # Base64
            r'^sk-[a-zA-Z0-9]{20,}',  # OpenAI API key
            r'^ghp_[a-zA-Z0-9]{36}',  # GitHub PAT
            r'^AKIA[0-9A-Z]{16}',  # AWS Access Key
        ]
        return any(re.search(p, content, re.IGNORECASE) for p in patterns)

    @classmethod
    def _extract_tags(cls, content: str, content_type: str) -> List[str]:
        """提取标签"""
        tags = [content_type]

        # 根据内容添加标签
        if re.search(r'\b(error|exception|bug|fix|debug)\b', content, re.IGNORECASE):
            tags.append("debug")
        if re.search(r'\b(config|configuration|settings|env)\b', content, re.IGNORECASE):
            tags.append("config")
        if re.search(r'\b(http|api|rest|graphql|endpoint)\b', content, re.IGNORECASE):
            tags.append("api")
        if re.search(r'\b(database|db|sql|query|mongo|redis)\b', content, re.IGNORECASE):
            tags.append("database")
        if re.search(r'\b(docker|container|kubernetes|k8s|pod)\b', content, re.IGNORECASE):
            tags.append("devops")

        return tags

    @classmethod
    def generate_summary(cls, content: str, max_length: int = 100) -> str:
        """生成内容摘要"""
        lines = content.strip().split('\n')
        first_line = lines[0].strip()

        if len(first_line) > max_length:
            return first_line[:max_length] + "..."

        if len(lines) > 1:
            return first_line + f" (+{len(lines)-1} lines)"

        return first_line
