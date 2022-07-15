from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


# создание условия передачи апдейта в хендлер
class IsDigit(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return (message.text.isdigit())