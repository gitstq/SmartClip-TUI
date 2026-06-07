"""
Clipboard Database Manager
剪贴板数据库管理模块
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class ClipItem:
    """剪贴板条目数据类"""
    id: Optional[int]
    content: str
    content_type: str  # text, code, url, email, command, password, image_path
    tags: List[str]
    favorite: bool
    created_at: str
    updated_at: str
    usage_count: int
    source_app: Optional[str]
    hash: str
    summary: Optional[str]


class ClipDatabase:
    """剪贴板数据库管理器"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            config_dir = Path.home() / ".config" / "smartclip"
            config_dir.mkdir(parents=True, exist_ok=True)
            db_path = config_dir / "clipboard.db"
        self.db_path = str(db_path)
        self.init_database()

    def init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    content_type TEXT DEFAULT 'text',
                    tags TEXT DEFAULT '[]',
                    favorite INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    usage_count INTEGER DEFAULT 0,
                    source_app TEXT,
                    hash TEXT UNIQUE NOT NULL,
                    summary TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_hash ON clips(hash)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_type ON clips(content_type)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_favorite ON clips(favorite)
            """)
            conn.commit()

    def _compute_hash(self, content: str) -> str:
        """计算内容哈希值"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:32]

    def add_clip(self, content: str, content_type: str = "text",
                 tags: Optional[List[str]] = None,
                 source_app: Optional[str] = None,
                 summary: Optional[str] = None) -> bool:
        """添加剪贴板条目"""
        if not content or len(content.strip()) == 0:
            return False

        content_hash = self._compute_hash(content)

        with sqlite3.connect(self.db_path) as conn:
            # 检查是否已存在
            cursor = conn.execute(
                "SELECT id FROM clips WHERE hash = ?", (content_hash,)
            )
            if cursor.fetchone():
                # 更新使用次数和时间
                conn.execute(
                    """UPDATE clips SET usage_count = usage_count + 1,
                        updated_at = ? WHERE hash = ?""",
                    (datetime.now().isoformat(), content_hash)
                )
                conn.commit()
                return True

            now = datetime.now().isoformat()
            tags_json = json.dumps(tags or [])

            conn.execute(
                """INSERT INTO clips
                    (content, content_type, tags, favorite, created_at,
                     updated_at, usage_count, source_app, hash, summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (content, content_type, tags_json, 0, now, now,
                 1, source_app, content_hash, summary)
            )
            conn.commit()
            return True

    def get_all_clips(self, limit: int = 100, offset: int = 0,
                      clip_type: Optional[str] = None,
                      favorite_only: bool = False) -> List[ClipItem]:
        """获取所有剪贴板条目"""
        query = "SELECT * FROM clips WHERE 1=1"
        params = []

        if clip_type:
            query += " AND content_type = ?"
            params.append(clip_type)
        if favorite_only:
            query += " AND favorite = 1"

        query += " ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()

            return [self._row_to_item(row) for row in rows]

    def search_clips(self, keyword: str, limit: int = 50) -> List[ClipItem]:
        """搜索剪贴板条目"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT * FROM clips
                   WHERE content LIKE ? OR summary LIKE ? OR tags LIKE ?
                   ORDER BY updated_at DESC LIMIT ?""",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", limit)
            )
            rows = cursor.fetchall()
            return [self._row_to_item(row) for row in rows]

    def toggle_favorite(self, clip_id: int) -> bool:
        """切换收藏状态"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE clips SET favorite = NOT favorite WHERE id = ?",
                (clip_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_clip(self, clip_id: int) -> bool:
        """删除剪贴板条目"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM clips WHERE id = ?", (clip_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def update_tags(self, clip_id: int, tags: List[str]) -> bool:
        """更新标签"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE clips SET tags = ? WHERE id = ?",
                (json.dumps(tags), clip_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute(
                "SELECT COUNT(*) FROM clips"
            ).fetchone()[0]
            favorites = conn.execute(
                "SELECT COUNT(*) FROM clips WHERE favorite = 1"
            ).fetchone()[0]
            type_counts = conn.execute(
                "SELECT content_type, COUNT(*) FROM clips GROUP BY content_type"
            ).fetchall()

            return {
                "total": total,
                "favorites": favorites,
                "type_counts": dict(type_counts)
            }

    def _row_to_item(self, row: sqlite3.Row) -> ClipItem:
        """将数据库行转换为ClipItem"""
        return ClipItem(
            id=row["id"],
            content=row["content"],
            content_type=row["content_type"],
            tags=json.loads(row["tags"]),
            favorite=bool(row["favorite"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            usage_count=row["usage_count"],
            source_app=row["source_app"],
            hash=row["hash"],
            summary=row["summary"]
        )
