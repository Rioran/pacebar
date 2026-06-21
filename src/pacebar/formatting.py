"""Display formatting helpers."""


def format_duration(total_seconds: float, show_hours: bool) -> str:
    """Format seconds as [-]HH:MM:SS, hiding the hours group when not needed."""
    is_negative = total_seconds < 0
    whole_seconds = int(abs(total_seconds))
    hours, remainder = divmod(whole_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if show_hours:
        body = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        body = f"{minutes:02d}:{seconds:02d}"
    return ("-" if is_negative else "") + body
