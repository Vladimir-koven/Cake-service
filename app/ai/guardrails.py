BLOCKED_TOPICS = ("цена", "стоимость", "сколько стоит", "прайс")


def check_user_message_safety(message: str) -> bool:
    """
    True — сообщение безопасно для передачи ИИ.
    False — эстафета уходит человеку (например, вопрос о цене).
    """
    lowered = message.lower()
    return not any(topic in lowered for topic in BLOCKED_TOPICS)
