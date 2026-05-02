"""
joi.utils.interface — Tema cyberpunk ASCII para Joi
"""

import time
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import box

console = Console()

NEON_PINK = "#FF2D95"
ELECTRIC_BLUE = "#00D4FF"
CYAN = "#00FFC8"
DEEP_PURPLE = "#7B2D8E"
SILVER = "#C0C0C0"

PROMPT_STYLE = f"bold {CYAN}"
NAME_STYLE = f"bold {NEON_PINK}"
ARROW_STYLE = f"{ELECTRIC_BLUE}"
RESPONSE_STYLE = SILVER
DIVIDER_STYLE = f"dim {DEEP_PURPLE}"


def banner():
    title = Text()
    title.append("  + ", style=ELECTRIC_BLUE)
    title.append("Joi", style=f"bold {NEON_PINK}")
    title.append("  +", style=ELECTRIC_BLUE)

    subtitle = Text("assistente pessoal autonoma", style=f"italic {DEEP_PURPLE}")

    panel = Panel(
        title,
        subtitle=subtitle,
        border_style=DEEP_PURPLE,
        width=46,
        padding=(0, 2),
        box=box.ASCII,
    )
    return panel


def prompt_user() -> str:
    console.print()
    return console.input(f"  [{PROMPT_STYLE}]>>[/] ").strip()


def typewrite(text: str, speed: float = 0.015):
    words = text.split(" ")
    for i, word in enumerate(words):
        buffer = " ".join(words[: i + 1])
        styled = Text(f"  ", style=f"bold {NEON_PINK}")
        styled.append("joi", style=f"bold {NEON_PINK}")
        styled.append(" >> ", style=ELECTRIC_BLUE)
        styled.append(buffer, style=SILVER)
        console.print(styled, end="\r" if i < len(words) - 1 else "\n")
        time.sleep(speed * len(word))


def spinner_ctx():
    """Retorna um objeto Status do rich. Chame .start() e .stop()."""
    return console.status(
        "  processando...",
        spinner="dots12",
        spinner_style=DEEP_PURPLE,
    )

    thread = threading.Thread(target=_spin, daemon=True)
    thread.start()
    return done


def stop_spinner(status):
    """Para o spinner."""
    try:
        status.stop()
    except Exception:
        pass


def divider():
    return Text("  ---", style=DIVIDER_STYLE)


def goodbye():
    text = Text()
    text.append(f"\n  ", style=NEON_PINK)
    text.append("*", style=NEON_PINK)
    text.append("  ate logo  ", style=ELECTRIC_BLUE)
    text.append("*", style=NEON_PINK)
    text.append("\n")
    return text


def error_msg(text: str):
    result = Text()
    result.append("  ", style=f"bold {NEON_PINK}")
    result.append("joi", style=f"bold {NEON_PINK}")
    result.append(" >> ", style=ELECTRIC_BLUE)
    result.append(text, style=NEON_PINK)
    return result


def status(msg: str):
    return Text(f"  {msg}", style=f"italic {DEEP_PURPLE}")
