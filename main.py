import asyncio

import aiogram  # Bot, Dispatcher(отправитель), executor(исполнитель)
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN

# создание бота
bot = aiogram.Bot(BOT_TOKEN)

# создание потока
loop = asyncio.get_event_loop()

# создание хранилища памяти
storage = MemoryStorage()


# cоздание диспатчера (загрузчика в поток или в память)
dp = aiogram.Dispatcher(bot, storage=storage)


def reg_middlewares(dp):
     #dp.setup_middleware()      # привязка мидлварей
     pass

import KalBot_handlers
def reg_handlers(dp):
     KalBot_handlers.reg_start(dp)     # привязка хандлеров
     KalBot_handlers.reg_stop(dp)
     KalBot_handlers.reg_kalory_1(dp)
     KalBot_handlers.reg_kalory_2(dp)
     KalBot_handlers.reg_kalory_3(dp)
     KalBot_handlers.reg_kalory_4(dp)
     KalBot_handlers.reg_error(dp)
     KalBot_handlers.reg_kalory_5(dp)


def reg_filters(dp):
     #dp.filters_factory.bind()  # привязка фильтров
     pass


if __name__ == "__main__":
     try:
          reg_middlewares(dp)
          reg_filters(dp)
          reg_handlers(dp)

          # запуск бота(получает сообщения и передает в dp(отправитель))
          aiogram.executor.start(dp, KalBot_handlers.admin_not())
          aiogram.executor.start_polling(dp)

     except (KeyboardInterrupt, SystemExit):
          pass