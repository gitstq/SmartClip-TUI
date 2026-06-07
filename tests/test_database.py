"""
Test Database
测试数据库模块
"""

import pytest
import tempfile
import os
from smartclip.database import ClipDatabase, ClipItem


class TestClipDatabase:
    """测试剪贴板数据库"""

    @pytest.fixture
    def db(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        db = ClipDatabase(db_path)
        yield db
        os.unlink(db_path)

    def test_add_clip(self, db):
        result = db.add_clip("test content", "text", ["tag1"])
        assert result is True

    def test_add_empty_clip(self, db):
        result = db.add_clip("", "text")
        assert result is False

    def test_get_all_clips(self, db):
        db.add_clip("content1", "text")
        db.add_clip("content2", "code")
        clips = db.get_all_clips()
        assert len(clips) == 2

    def test_search_clips(self, db):
        db.add_clip("hello world", "text")
        db.add_clip("goodbye world", "text")
        results = db.search_clips("hello")
        assert len(results) == 1
        assert results[0].content == "hello world"

    def test_toggle_favorite(self, db):
        db.add_clip("test", "text")
        clips = db.get_all_clips()
        clip_id = clips[0].id

        db.toggle_favorite(clip_id)
        clips = db.get_all_clips(favorite_only=True)
        assert len(clips) == 1

    def test_delete_clip(self, db):
        db.add_clip("test", "text")
        clips = db.get_all_clips()
        clip_id = clips[0].id

        db.delete_clip(clip_id)
        clips = db.get_all_clips()
        assert len(clips) == 0

    def test_update_tags(self, db):
        db.add_clip("test", "text", ["old"])
        clips = db.get_all_clips()
        clip_id = clips[0].id

        db.update_tags(clip_id, ["new1", "new2"])
        clips = db.get_all_clips()
        assert clips[0].tags == ["new1", "new2"]

    def test_get_stats(self, db):
        db.add_clip("test1", "text")
        db.add_clip("test2", "code")
        stats = db.get_stats()
        assert stats["total"] == 2
        assert "text" in stats["type_counts"]

    def test_duplicate_handling(self, db):
        db.add_clip("duplicate", "text")
        db.add_clip("duplicate", "text")
        clips = db.get_all_clips()
        assert len(clips) == 1
        assert clips[0].usage_count == 2
