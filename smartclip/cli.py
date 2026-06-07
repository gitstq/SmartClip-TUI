"""
SmartClip CLI Commands
SmartClip 命令行接口
"""

import click
from typing import Optional
from .database import ClipDatabase
from .classifier import ContentClassifier
from .clipboard_monitor import ClipboardMonitor


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """SmartClip - 智能剪贴板管理器"""
    pass


@cli.command()
def tui():
    """启动TUI界面"""
    from .ui import run_app
    run_app()


@cli.command()
@click.argument("content", required=False)
@click.option("--type", "-t", help="内容类型")
@click.option("--tag", "-g", multiple=True, help="标签")
def add(content: Optional[str], type: Optional[str], tag: tuple):
    """添加剪贴板内容"""
    db = ClipDatabase()

    if not content:
        monitor = ClipboardMonitor(lambda x: None)
        content = monitor.get_current()
        if not content:
            click.echo("❌ 剪贴板为空，请提供内容")
            return

    content_type = type or ContentClassifier.classify(content)[0]
    tags = list(tag) if tag else ContentClassifier.classify(content)[1]

    if db.add_clip(content, content_type, tags):
        click.echo(f"✅ 已添加 [{content_type}]: {content[:50]}...")
    else:
        click.echo("❌ 添加失败")


@cli.command()
@click.option("--limit", "-l", default=20, help="显示数量")
@click.option("--type", "-t", help="筛选类型")
@click.option("--favorite", "-f", is_flag=True, help="仅显示收藏")
def list(limit: int, type: Optional[str], favorite: bool):
    """列出剪贴板历史"""
    db = ClipDatabase()
    clips = db.get_all_clips(limit=limit, clip_type=type, favorite_only=favorite)

    if not clips:
        click.echo("📭 剪贴板为空")
        return

    click.echo(f"📋 剪贴板历史 (共 {len(clips)} 条):\n")

    type_icons = {
        "text": "📝", "code": "💻", "url": "🔗", "email": "📧",
        "command": "⚡", "json": "📊", "path": "📁", "password": "🔒"
    }

    for clip in clips:
        icon = type_icons.get(clip.content_type, "📄")
        fav = "⭐" if clip.favorite else "  "
        summary = clip.summary or clip.content[:60]
        if len(summary) > 60:
            summary = summary[:60] + "..."

        click.echo(
            f"{fav} [{clip.id:4d}] {icon} {clip.content_type:8s} | "
            f"{summary} | 使用:{clip.usage_count}"
        )


@cli.command()
@click.argument("keyword")
@click.option("--limit", "-l", default=20, help="显示数量")
def search(keyword: str, limit: int):
    """搜索剪贴板内容"""
    db = ClipDatabase()
    clips = db.search_clips(keyword, limit)

    if not clips:
        click.echo(f"🔍 未找到包含 '{keyword}' 的内容")
        return

    click.echo(f"🔍 搜索结果 (共 {len(clips)} 条):\n")
    for clip in clips:
        fav = "⭐" if clip.favorite else "  "
        summary = clip.summary or clip.content[:80]
        click.echo(f"{fav} [{clip.id}] {summary}")


@cli.command()
@click.argument("clip_id", type=int)
def copy(clip_id: int):
    """复制指定ID的内容到剪贴板"""
    db = ClipDatabase()
    clips = db.get_all_clips(limit=1000)

    clip = next((c for c in clips if c.id == clip_id), None)
    if not clip:
        click.echo(f"❌ 未找到 ID {clip_id}")
        return

    monitor = ClipboardMonitor(lambda x: None)
    if monitor.set_clipboard(clip.content):
        click.echo(f"✅ 已复制: {clip.content[:100]}...")
    else:
        click.echo("❌ 复制失败")


@cli.command()
@click.argument("clip_id", type=int)
def delete(clip_id: int):
    """删除指定ID的内容"""
    db = ClipDatabase()
    if db.delete_clip(clip_id):
        click.echo(f"🗑️ 已删除 ID {clip_id}")
    else:
        click.echo(f"❌ 未找到 ID {clip_id}")


@cli.command()
@click.argument("clip_id", type=int)
def favorite(clip_id: int):
    """切换收藏状态"""
    db = ClipDatabase()
    if db.toggle_favorite(clip_id):
        click.echo(f"⭐ 已切换 ID {clip_id} 的收藏状态")
    else:
        click.echo(f"❌ 未找到 ID {clip_id}")


@cli.command()
def stats():
    """显示统计信息"""
    db = ClipDatabase()
    stats = db.get_stats()

    click.echo("📊 SmartClip 统计信息:\n")
    click.echo(f"  总计条目: {stats['total']}")
    click.echo(f"  收藏条目: {stats['favorites']}")
    click.echo(f"  类型分布:")
    for type_name, count in stats['type_counts'].items():
        click.echo(f"    - {type_name}: {count}")


@cli.command()
def clear():
    """清空所有剪贴板历史"""
    if click.confirm("⚠️ 确定要清空所有剪贴板历史吗?"):
        db = ClipDatabase()
        # 获取所有并删除
        clips = db.get_all_clips(limit=10000)
        for clip in clips:
            db.delete_clip(clip.id)
        click.echo("🗑️ 已清空所有历史")


if __name__ == "__main__":
    cli()
