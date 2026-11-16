from fastapi import APIRouter, HTTPException
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from pydantic import BaseModel

from app.ai.guardrails import check_user_message_safety
from app.ai.prompts import SYSTEM_PROMPT
from app.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])

# Инициализируем клиент один раз (глобально), чтобы не пересоздавать при каждом запросе
giga = GigaChat(
    credentials=settings.gigachat_credentials,
    scope=settings.gigachat_scope,
    model=settings.gigachat_model,
    verify_ssl_certs=False,  # Временно для локалки! (Позже заменим на путь к сертификату)
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    is_human_needed: bool = False


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Прогоняем через предохранитель (guardrails)
    if not check_user_message_safety(request.message):
        return ChatResponse(
            reply="Уточню стоимость и детали у нашего кондитера. Он свяжется с вами в ближайшее время.",
            is_human_needed=True,
        )

    # 2. Если безопасно — отправляем в GigaChat и формируем полезную нагрузку с системным промптом
    try:
        payload = Chat(
            messages=[
                Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT),
                Messages(role=MessagesRole.USER, content=request.message),
            ]
        )

        response = giga.chat(payload)
        return ChatResponse(reply=response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обращении к ИИ: {str(e)}") from e
