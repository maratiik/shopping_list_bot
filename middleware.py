from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from typing import Callable, Dict, Any, Awaitable


class SessionMiddleware(BaseMiddleware):

    def __init__(self, engine: Engine = None):
        self.engine = engine 
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if self.engine is not None:
            data['session'] = Session(self.engine)
        return await handler(event, data)
