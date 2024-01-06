import config

GREETINGS = """Привееет!
Это Telegram-бот книжного клуба Ботаним.
Здесь можно посмотреть список книг, которые мы читали и планируем читать, \
а также проголосовать за следующую книгу.

Присоединяйся к клубу: https://botanim.to.digital

Команды бота:

/start - приветственное сообщение 
/help - справка
/allbooks - все книги, который есть в нашем списке
/allready - прочитанные книги 
/now - книга, которую сейчас читаем 
/vote - проголосовать за следующую книгу
/voteresults - результаты голосования
/voteresultsgraph - результаты голосования в графике
"""

HELP = """
Наш книжный клуб работает по ежемесячной подписке, которая \
стоит 1500 руб/мес. Подписка работает через бот @donate, для того, чтобы \
подписаться, перейдите по этой ссылке: https://t.me/+IyGKU9EIGP5 jMTky
Если у вас не получается подписаться или есть иные вопросы, напишите на почту \
sterxarl6.ru
"""

VOTE = """
Выше тебе отправили все книги, за которые можно проголосвать. Вжууух!

<b>Тебе нужно выбрать 3 книги. </b> 

Пришли в ответном сообщение номера книг, которые ты хочешь прочитать. Номер можно разделить пробелами, запятыми, переносами строк

Обрати внимание, что порядок важен! 
"""

VOTE_PROCESS_INCORRECT_INPUT = f"""Не смог прочесть номер книги из твоего сообщения. Напиши {config.VOTE_ELEMENTS_COUNT} разных номера книг в сообщении.

Напиши например так:
{' '.join(map(str, [i for i in range(1, config.VOTE_ELEMENTS_COUNT + 1)]))}

"""

VOTE_PROCESS_INCORRECT_BOOKS = f"""
Ты вел некорректные номера книг.

Напиши например так:
{' '.join(map(str, [i for i in range(1, config.VOTE_ELEMENTS_COUNT + 1)]))}

"""

NO_ACTUAL_VOTING = """
Сейчас нет голосования 
"""
NO_VOTE_RESULTS = """
Нет результатов голосования
"""
