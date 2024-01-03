create table bot_user(
    telegram_id bigint not null UNIQUE,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP not null
);

create table book_category(
 id integer primary key,
 created_at timestamp DEFAULT CURRENT_TIMESTAMP not null,
 name varchar(60) not null unique,
 ordering integer not null unique
);

create table book(
    id integer PRIMARY Key,
    created_at timestamp default current_timestamp not null,
    name text, 
    ordering not null,
    read_start date,
    read_finish date,
    category_id integer,
    foreign key(category_id) REFERENCES book_category(id),
    unique(category_id, ordering)
);

-- Голосование 
create table voting(
    id integer primary key,
    voting_start timestamp not null unique,
    voting_finish timestamp not null unique
);
create table vote(
    id integer primary key,
    vote_id integer,
    user_id integer,
    first_book integer,
    second_book integer,
    third_book integer,
    foreign key(vote_id) REFERENCES voting(id),
    foreign key(user_id) REFERENCES bot_user(telegram_id),
    foreign key(first_book) REFERENCES book(id),
    foreign key(second_book) REFERENCES book(id),
    foreign key(third_book) REFERENCES book(id)
);

insert into book_category (name, ordering) values 
  ('Как писать хорошо, а нехорошо не писать', 10),
  ('Тестирование', 20),
  ('Python', 30),
  ('Go', 40),
  ('Rust', 50),
  ('JavaScript', 60),
  ('Linux ', 70),
  ('Алгоритмы', 80),
  ('БД', 90),
  ('Безопасность', 100),
  ('Большие системы', 110),
  ('Фронтенд', 120),
  ('Machine Learning', 130),
  ('Another interesting', 140),
  ('Софт-скилы, проектная работа', 150);

insert into book (name, category_id, ordering) values 
  ('Чистый код :: Роберт Мартин', 1, 1),
  ('Идеальный программист :: Роберт Мартин', 1, 2),
  ('Чистая архитектура :: Роберт Мартин', 1, 3),
  ('Идеальная работа :: Роберт Мартин', 1, 4),
  ('Совершенный код :: Стив Макконнелл', 1, 5),
  ('Паттерны объектно-ориентированного проектирования :: Гамма Эрих, Хелм Ричард, Джонсон Роберт, Влиссидес Джон', 1, 6),
  ('Head First. Паттерны проектирования. 2-е издание :: Эрик Фримен, Элизабет Робсон', 1, 7),
  ('Шаблоны корпоративных приложений :: Мартин Фаулер', 1, 8),
  ('Шаблоны интеграции корпоративных приложений :: Бобби Вульф, Грегор Хоп', 1, 9),
  ('Предметно-ориентированное проектирование :: Эрик Эванс', 1, 10),
  ('Реализация методов предметно-ориентированного проектирования :: Вон Вернон', 1, 11),
  ('Пять строк кода :: Кристиан Клаусен', 1, 12),
  ('Рефакторинг. Улучшение существующего кода :: Мартин Фаулер ', 1, 13),
  ('Программируй & типизируй :: Влад Ришкуция', 1, 14),
  ('A Philosophy of Software Design, 2nd edition :: John Ousterhout', 1, 15),
  ('Эффективная работа с унаследованным кодом :: Майкл Физерс', 1, 16),

  ('Экстремальное программирование: разработка через тестирование :: Бек Кент', 2, 1),
  ('Принципы юнит-тестирования :: Хориков Владимир', 2, 2),
  ('Python. Разработка на основе тестирования :: Персиваль Гарри', 2, 3),
  ('Эффективное тестирование программного обеспечения :: Аниче Маурисио', 2, 4),

  ('Начинаем Программировать на Python. 5 издание :: Тонни Гэддис', 3, 1),
  ('Простой Python. 2 издание :: Билл Любанович', 3, 2),
  ('Effective Python: 90 Specific Ways to Write Better Python :: Brett Slatkin', 3, 3),
  ('Python на практике :: Марк Саммерфильд', 3, 4),
  ('Python к вершинам мастерства :: Лучано Рамальо', 3, 5),
  ('Asyncio и конкурентное программирование :: Мэттью Фаулер', 3, 6),
  ('Паттерны разработки на Python :: Гарри Персиваль. Боб Грегори', 3, 7),
  ('Clean Code in Python, Second Edition :: Mariano Anaya', 3, 8),
  ('Python Tricks :: Dan Bader, он же Чистый Python тонкости программирования для профи', 3, 9),
  ('Высокопроизводительные Python-приложения. Практическое руководство по эффективному программированию, 2 издание :: Горелик Миша', 3, 10),
  ('Автоматизация рутинных задач с помощью Python. 2 издание :: Эл Свейгарт', 3, 11),
  ('Внутри CPYTHON: гид по интерпретатору Python :: Энтони Шоу', 3, 12),
  ('Стандартная библиотека Python 3. Справочник с примерами :: Хеллман Даг', 3, 13),

  ('Язык программирования Go :: Алан Донован, Брайан Керниган', 4, 1),
  ('Go на практике :: Мэтт Батчер, Мэтт Фарина', 4, 2),
  ('Go. Идиомы и паттерны проектирования :: Джон Боднер', 4, 3),

  ('Программирование на Rust. Официальный гайд', 5, 1),
  ('Программирование на языке Rust :: Джейсон Орендорф, Джим Блэнди', 5, 2),
  ('Rust в действии :: Тим Макнамара', 5, 3),
  ('Zero To Production In Rust :: Luca Palmieri', 5, 4),

  ('Выразительный JavaScript. Современное веб-программирование :: Хавербеке Марейн', 6, 1),
  ('Вы не знаете JS: Начните и Совершенствуйтесь :: Kyle Simpson', 6, 2),
  ('Вы не знаете JS: Область видимости и замыкания :: Kyle Simpson', 6, 3),
  ('Вы не знаете JS: this и Прототипы Объектов :: Kyle Simpson', 6, 4),
  ('Вы не знаете JS: Типы и грамматика :: Kyle Simpson', 6, 5),
  ('Вы не знаете JS: Асинхронность и Производительность :: Kyle Simpson', 6, 6),
  ('Вы не знаете JS: ES6 и не только :: Kyle Simpson', 6, 7),
  ('Тестирование JavaScript :: Лукас Коста', 6, 8),

  ('Командная строка Linux. Полное руководство :: Шоттс Уильям', 7, 1),
  ('Linux. Необходимый код и команды :: Граннеман Скотт', 7, 2),
  ('Библия Linux. 10-е издание :: Негус Кристофер', 7, 3),

  ('Грокаем алгоритмы :: Бхаргава Адитья', 8, 1),
  ('Алгоритмы для начинающих. Теория и практика для разработчика :: Луридас Панос (проще Кормена, глубже, чем Грокаем)', 8, 2),
  ('Алгоритмы: построение и анализ. 3-е издание :: Томас Кормен', 8, 3),
  ('Тим Рафгарден, серия Совершенный алгоритм', 8, 4),

  ('Основы технологий баз данных :: Борис Новиков, Екатерина Горшкова', 9, 1),
  ('PostgreSQL 14 изнутри :: Егор Рогов', 9, 2),
  ('Оптимизация запросов в PostgreSQL :: Борис Новиков, Генриэтта Домбровская', 9, 3),
  ('PostgreSQL. Основы языка SQL :: Евгений Моргунов', 9, 4),
  ('PostgreSQL 11. Мастерство разработки :: Ганс-Юрген Шениг', 9, 5),
  ('NoSQL Distilled :: Мартин Фаулер', 9, 6),

  ('Hacking for Dummies :: Kevin Beaver', 10, 1),
  ('Безопасность web-приложений :: Эндрю Хоффман', 10, 2),
  ('Хакинг: искусство эксплойта. 2-е изд. :: Эриксон Джон', 10, 3),
  ('Высоконагруженные приложения. Программирование, масштабирование, поддержка :: Мартин Клеппман', 11, 1),
  ('Облачные архитектуры. Разработка устойчивых и экономичных облачных приложений :: Том Лащевски, Камаль Арора, Эрик Фарр, Пийюм Зонуз', 11, 2),
  ('System Design :: Алекс Сюй', 11, 3),

  ('Разработка интерфейсов. Паттерны проектирования. 3-е издание :: Дженифер Тидвелл, Чарли Брюэр, Эйнн Валенсия', 12, 1),
  ('Accessibility for Everyone :: Laura Kalbag', 12, 2),
  ('Refactoring UI :: Adam Wathan, Steve Schoger', 12, 3),
  ('Не заставляйте меня думать. Веб-юзабилити и здравый смысл. 3-е издание :: Стив Круг', 12, 4),
  ('Pro HTML5 Accessibility :: Joshue O. Connor', 12, 5),
  ('CSS для профи :: Грант Кит', 12, 6),
  ('Интерфейс. Новые направления в проектировании компьютерных систем :: Джеф Раскин', 12, 7),

  ('Hands-On Machine Learning with Scikit-Learn, Keras, and Tensorflow: Concepts, Tools, and Techniques to Build Intelligent Systems. 2nd Edition :: Aurélien Géron', 13, 1),
  ('Python и машинное обучение :: Себастьян Рашка', 13, 2),
  ('Python и машинное обучение. Машинное и глубокое обучение с использованием Python, scikit-learn и TensorFlow 2 :: Мирджалили Вахид, Рашка Себастьян', 13, 3),
  ('Практическая статистика для специалистов Data Science. 2-е изд. :: Брюс Питер', 13, 4),
  ('Глубокое обучение на Python. 2 издание :: Шолле Франсуа', 13, 5),
  ('Deep Learning for Vision Systems :: Mohamed Elgendy', 13, 6),
  ('Python для сложных задач: наука о данных и машинное обучение :: Вандер Плас Дж.', 13, 7),
  ('Data Science Наука о данных с нуля :: Грас Джоэл', 13, 8),
  ('Python и анализ данных :: Маккини Уэс', 13, 9),
  ('An Introduction to Statistical Learning :: Gareth James, Daniela Witten, Trevor Hastie, Rob Tibshirani (для новичков с матбазой)', 13, 10),
  ('Bayesian Reasoning and Machine Learning :: David Barber (для продвинутых)', 13, 11),
  ('Pattern Recognition and Machine Learning :: Кристофер Бишоп (для продвинутых)', 13, 12),

  ('LLVM. Инфраструктура для разработки компиляторов :: Аулер Рафаэль, Лопес Бруно Кардос', 14, 1),
  ('Время UNIX. A History and a Memoir :: Брайан Керниган', 14, 2),
  ('Git для профессионального программиста :: Штрауб Бен, Чакон Скотт', 14, 3),
  ('Теоретический минимум по Computer Science. Все что нужно программисту и разработчику :: Фило Владстон Феррейра', 14, 4),
  ('Микросервисы и контейнеры Docker :: Парминдер Сингх Кочер', 14, 5),
  ('Практическое использование Vim :: Дрю Нейл', 14, 6),
  ('IT как оружие :: Брэд Смит, Кэрол Энн Браун', 14, 7),
  ('Ум программиста. Как понять и осмыслить любой код :: Фелин Херманс', 14, 8),
  ('Делай как в Google. Разработка программного обеспечения :: Райт Хайрам, Маншрек Том', 14, 9),
  ('Код: тайный язык информатики :: Чарльз Петцольд', 14, 10),
  ('Структура и Интерпретация Компьютерных Программ :: Сассман Джеральд Джей, Абельсон Харольд', 14, 11),
  ('Проект «Феникс». Роман о том, как DevOps меняет бизнес к лучшему :: Спаффорд Джордж, Бер Кевин', 14, 12),
  ('Microservices Patterns :: Chris Richardson', 14, 13),

  ('Наш код. Ремесло, профессия, искусство :: Егор Бугаенко', 15, 1),
  ('Программист-прагматик. Путь от подмастерья к мастеру :: Э. Хант, Д. Томас', 15, 2),
  ('Джедайские техники :: Дорофеев Максим', 15, 3),
  ('Визуализируйте работу :: Доминика Деграндис', 15, 4),
  ('Как пасти котов :: Рейнвотер Дж. Ханк', 15, 5),
  ('Мифический человеко-месяц, или Как создаются программные системы :: Брукс Фредерик', 15, 6),
  ('Deadline. Роман об управлении проектами :: Том Демарко', 15, 7),
  ('Сделано. Проектный менеджмент на практике :: Скотт Беркун', 15, 8),
  ('Думай медленно… решай быстро :: Даниэль Канеман', 15, 9),
  ('Стартап: Настольная книга основателя :: Стив Бланк, Боб Дорф', 15, 10),
  ('От нуля к единице :: Питер Тиль', 15, 11),
  ('Бизнес с нуля :: Эрик Рис', 15, 12),
  ('Rework: бизнес без предрассудков :: Джейсон Фрайд, Дэвид Хайнемайер Хенссон', 15, 13),
  ('Как привести дела в порядок :: Дэвид Аллен', 15, 14);

update book set 
read_start='2022-11-21',
read_finish='2022-12-18'
where name='Чистый код :: Роберт Мартин';

update book set 
read_start='2022-12-18',
read_finish='2022-12-31'
where name='Теоретический минимум по Computer Science. Все что нужно программисту и разработчику :: Фило Владстон Феррейра';

update book set 
read_start='2023-01-01',
read_finish='2023-02-12'
where name='PostgreSQL. Основы языка SQL :: Евгений Моргунов';