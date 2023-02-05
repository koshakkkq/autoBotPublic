import logging


from create import dp

@dp.errors_handlers()
async def error_handler(update, exception):
    logging.exception(f'Update: {update}\n Exception {exception}')