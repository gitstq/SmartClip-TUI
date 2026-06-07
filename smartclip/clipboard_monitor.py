"""
Clipboard Monitor
剪贴板监控模块 - 跨平台支持
"""

import threading
import time
from typing import Callable, Optional

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


class ClipboardMonitor:
    """剪贴板监控器"""

    def __init__(self, callback: Callable[[str], None], interval: float = 0.5):
        self.callback = callback
        self.interval = interval
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._last_content: Optional[str] = None

    def start(self):
        """启动监控"""
        if not PYPERCLIP_AVAILABLE:
            print("Warning: pyperclip not available, clipboard monitoring disabled")
            return

        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """停止监控"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _monitor_loop(self):
        """监控循环"""
        while self._running:
            try:
                current = pyperclip.paste()
                if current and current != self._last_content:
                    self._last_content = current
                    self.callback(current)
            except Exception as e:
                print(f"Clipboard monitor error: {e}")
            time.sleep(self.interval)

    def get_current(self) -> Optional[str]:
        """获取当前剪贴板内容"""
        if not PYPERCLIP_AVAILABLE:
            return None
        try:
            return pyperclip.paste()
        except Exception:
            return None

    def set_clipboard(self, content: str) -> bool:
        """设置剪贴板内容"""
        if not PYPERCLIP_AVAILABLE:
            return False
        try:
            pyperclip.copy(content)
            self._last_content = content
            return True
        except Exception as e:
            print(f"Failed to set clipboard: {e}")
            return False
