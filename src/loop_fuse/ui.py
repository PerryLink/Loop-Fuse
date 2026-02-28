from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import List, Tuple, Any

def display_circuit_break_warning(
    history: List[Tuple[str, Any]],
    fingerprint: str,
    cost_saved: float
) -> None:
    """显示熔断警告"""
    console = Console()

    repeat_count = sum(1 for fp, _ in history if fp == fingerprint)

    warning_text = f"""[bold red]⚠️  循环检测！系统已熔断 ⚠️[/bold red]

指纹: {fingerprint[:16]}...
重复次数: {repeat_count}
总调用次数: {len(history)}
节省成本: ${cost_saved:.4f}
    """

    console.print(Panel(warning_text, border_style="red", title="LOOP FUSE"))

    table = Table(title="循环历史", show_header=True)
    table.add_column("#", style="dim")
    table.add_column("指纹", style="cyan")
    table.add_column("操作", style="yellow")

    for i, (fp, action) in enumerate(history, 1):
        marker = "🔴" if fp == fingerprint else "⚪"
        table.add_row(
            f"{marker} {i}",
            fp[:8] + "...",
            str(action)[:50]
        )

    console.print(table)
