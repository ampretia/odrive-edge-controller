def log(data) -> str:
    text = "["
    for v in list(data):
        text += f"{v:02X} "

    text = text.strip()
    text += "]"
    return text