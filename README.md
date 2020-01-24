# Парсер книг с сайта tululu.org

Парсер скачивает подборку фантастических книг с сайта [tululu.org](http://tululu.org/l55/).

Скачивается сама книга, изображение книги, а также в файл записывается информация об авторе, названии, комментарии к книге.
### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Аргументы

Создайте файл `.env` и в него пропишите:
```
BOOK_INFORMATION_FILE_NAME='book_informations.json' #ваше название файла, куда будет сохраняться информация по книгам.
``` 

Для запуска программы необходимо написать в терминале следующее:
```commandline
python3 main.py
```

Также у скрипта есть два аргумента `--start_page`, страницы с которой начинается скачивание, по умолчанию 1,
 и `--end_page`, страница на которой заканчивается скачивание, по умолчанию 701.

```commandline
python3 main.py --start_page 100 --end_page 200
```
В этом случае скачаются книги со страницы 100 по страницу 200 с сайта [tululu.org](http://tululu.org/l55/).

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).