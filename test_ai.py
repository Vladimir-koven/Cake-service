from gigachat import GigaChat

from app.config import settings

giga = GigaChat(
    credentials=settings.gigachat_credentials,
    scope=settings.gigachat_scope,
    model=settings.gigachat_model,
    verify_ssl_certs=False,  # Временно, для локальной проверки!
)

try:
    response = giga.chat("Привет! Ты готов помогать с заказами тортов?")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Ошибка: {e}")
