"""
SmartClip TUI Interface
SmartClip 终端用户界面
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import (
    Header, Footer, DataTable, Input, Static, Button,
    Label, ListView, ListItem, TextArea, TabbedContent, TabPane
)
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from typing import List, Optional

from .database import ClipDatabase, ClipItem
from .classifier import ContentClassifier
from .clipboard_monitor import ClipboardMonitor


class ClipDetailScreen(Screen):
    """剪贴板详情屏幕"""

    def __init__(self, clip: ClipItem, db: ClipDatabase):
        super().__init__()
        self.clip = clip
        self.db = db

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header(show_clock=True)
            yield Static(f"📋 剪贴板详情 (ID: {self.clip.id})", classes="title")

            with Container(classes="detail-container"):
                yield Static(f"类型: {self.clip.content_type}", classes="info")
                yield Static(f"标签: {', '.join(self.clip.tags) or '无'}", classes="info")
                yield Static(f"收藏: {'⭐' if self.clip.favorite else '☆'}", classes="info")
                yield Static(f"使用次数: {self.clip.usage_count}", classes="info")
                yield Static(f"创建时间: {self.clip.created_at}", classes="info")
                yield Static(f"更新时间: {self.clip.updated_at}", classes="info")

                yield Static("内容:", classes="label")
                text_area = TextArea(text=self.clip.content, read_only=True)
                text_area.styles.height = "20"
                yield text_area

            with Horizontal(classes="button-row"):
                yield Button("📋 复制到剪贴板", id="copy")
                yield Button("⭐ 切换收藏", id="favorite")
                yield Button("🏷️ 编辑标签", id="tags")
                yield Button("🗑️ 删除", id="delete", variant="error")
                yield Button("🔙 返回", id="back")

            yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "copy":
            monitor = ClipboardMonitor(lambda x: None)
            if monitor.set_clipboard(self.clip.content):
                self.notify("✅ 已复制到剪贴板", severity="information")
            else:
                self.notify("❌ 复制失败", severity="error")

        elif button_id == "favorite":
            self.db.toggle_favorite(self.clip.id)
            self.clip.favorite = not self.clip.favorite
            self.notify("⭐ 收藏状态已更新", severity="information")
            self.app.pop_screen()

        elif button_id == "delete":
            self.db.delete_clip(self.clip.id)
            self.notify("🗑️ 已删除", severity="information")
            self.app.pop_screen()

        elif button_id == "back":
            self.app.pop_screen()


class SmartClipApp(App):
    """SmartClip TUI 应用"""

    CSS = """
    Screen { align: center middle; }

    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding: 1;
    }

    .info {
        padding: 0 1;
        color: $text;
    }

    .label {
        text-style: bold;
        padding: 1 1 0 1;
    }

    .detail-container {
        width: 100%;
        height: auto;
        padding: 1;
    }

    .button-row {
        align: center middle;
        padding: 1;
    }

    .button-row Button {
        margin: 0 1;
    }

    DataTable {
        width: 100%;
        height: 1fr;
    }

    Input {
        width: 100%;
    }

    .stats {
        text-align: center;
        color: $text-muted;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("r", "refresh", "刷新"),
        Binding("f", "toggle_favorite", "收藏"),
        Binding("d", "delete", "删除"),
        Binding("s", "search", "搜索"),
        Binding("c", "copy", "复制"),
        Binding("n", "new_clip", "新建"),
    ]

    clips = reactive(List[ClipItem])
    current_filter = reactive(str)

    def __init__(self):
        super().__init__()
        self.db = ClipDatabase()
        self.monitor: Optional[ClipboardMonitor] = None
        self.selected_clip: Optional[ClipItem] = None
        self.show_favorites_only = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical():
            yield Static("🚀 SmartClip-TUI - 智能剪贴板管理器", classes="title")

            with Horizontal():
                yield Input(placeholder="🔍 搜索剪贴板内容...", id="search")
                yield Button("⭐ 收藏", id="filter_favorite")
                yield Button("🔄 刷新", id="refresh")

            yield DataTable(id="clip_table")

            yield Static(id="stats", classes="stats")

        yield Footer()

    def on_mount(self) -> None:
        """挂载时初始化"""
        self.clips = self.db.get_all_clips(limit=100)
        self.update_table()
        self.update_stats()

        # 启动剪贴板监控
        self.monitor = ClipboardMonitor(self._on_clipboard_change)
        self.monitor.start()

    def _on_clipboard_change(self, content: str) -> None:
        """剪贴板变化回调"""
        content_type, tags = ContentClassifier.classify(content)
        summary = ContentClassifier.generate_summary(content)

        self.db.add_clip(
            content=content,
            content_type=content_type,
            tags=tags,
            summary=summary
        )

        # 刷新显示
        self.call_later(self.refresh_clips)

    def refresh_clips(self) -> None:
        """刷新剪贴板列表"""
        if self.current_filter:
            self.clips = self.db.search_clips(self.current_filter)
        else:
            self.clips = self.db.get_all_clips(
                limit=100,
                favorite_only=self.show_favorites_only
            )
        self.update_table()
        self.update_stats()

    def update_table(self) -> None:
        """更新表格"""
        table = self.query_one("#clip_table", DataTable)
        table.clear(columns=True)

        table.add_columns("ID", "类型", "内容摘要", "标签", "⭐", "使用", "时间")

        type_icons = {
            "text": "📝",
            "code": "💻",
            "url": "🔗",
            "email": "📧",
            "command": "⚡",
            "json": "📊",
            "path": "📁",
            "password": "🔒",
            "ip_address": "🌐",
        }

        for clip in self.clips:
            icon = type_icons.get(clip.content_type, "📄")
            summary = clip.summary or clip.content[:50] + "..."
            if len(summary) > 50:
                summary = summary[:50] + "..."

            tags_str = ", ".join(clip.tags[:3]) if clip.tags else ""
            favorite = "⭐" if clip.favorite else ""

            table.add_row(
                str(clip.id),
                f"{icon} {clip.content_type}",
                summary,
                tags_str,
                favorite,
                str(clip.usage_count),
                clip.updated_at[:16]
            )

    def update_stats(self) -> None:
        """更新统计信息"""
        stats = self.db.get_stats()
        stats_widget = self.query_one("#stats", Static)
        stats_widget.update(
            f"📊 总计: {stats['total']} | ⭐ 收藏: {stats['favorites']} | "
            f"📝 类型分布: {', '.join(f'{k}:{v}' for k, v in stats['type_counts'].items())}"
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        """搜索输入变化"""
        self.current_filter = event.value
        if self.current_filter:
            self.clips = self.db.search_clips(self.current_filter)
        else:
            self.clips = self.db.get_all_clips(favorite_only=self.show_favorites_only)
        self.update_table()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        button_id = event.button.id

        if button_id == "refresh":
            self.refresh_clips()
            self.notify("🔄 已刷新", severity="information")

        elif button_id == "filter_favorite":
            self.show_favorites_only = not self.show_favorites_only
            self.refresh_clips()
            status = "已开启" if self.show_favorites_only else "已关闭"
            self.notify(f"⭐ 收藏筛选{status}", severity="information")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """表格行选中事件"""
        if event.row_key is None:
            return

        row_index = int(str(event.row_key))
        if 0 <= row_index < len(self.clips):
            self.selected_clip = self.clips[row_index]
            self.push_screen(ClipDetailScreen(self.selected_clip, self.db))

    def action_refresh(self) -> None:
        """刷新动作"""
        self.refresh_clips()

    def action_search(self) -> None:
        """搜索动作"""
        self.query_one("#search", Input).focus()

    def action_quit(self) -> None:
        """退出动作"""
        if self.monitor:
            self.monitor.stop()
        self.exit()

    def action_copy(self) -> None:
        """复制选中项"""
        if self.selected_clip:
            monitor = ClipboardMonitor(lambda x: None)
            monitor.set_clipboard(self.selected_clip.content)
            self.notify("✅ 已复制", severity="information")

    def action_toggle_favorite(self) -> None:
        """切换收藏"""
        if self.selected_clip:
            self.db.toggle_favorite(self.selected_clip.id)
            self.refresh_clips()

    def action_delete(self) -> None:
        """删除选中项"""
        if self.selected_clip:
            self.db.delete_clip(self.selected_clip.id)
            self.refresh_clips()
            self.notify("🗑️ 已删除", severity="information")

    def action_new_clip(self) -> None:
        """新建剪贴板条目"""
        # 获取当前剪贴板内容
        monitor = ClipboardMonitor(lambda x: None)
        content = monitor.get_current()
        if content:
            content_type, tags = ContentClassifier.classify(content)
            self.db.add_clip(content, content_type, tags)
            self.refresh_clips()
            self.notify("✅ 已添加新条目", severity="information")


def run_app():
    """运行TUI应用"""
    app = SmartClipApp()
    app.run()


if __name__ == "__main__":
    run_app()
