<h4>Данный репозиторий разработан по тестовому заданию от компании Workmate.<br>
Репозиторий содержит скрипт (<code>main.py</code>), который формирует отчёт по эффективности по должностям.</h4>
<hr>
Пример готового отчёта:
<br>
<img width="313" height="338" alt="image" src="https://github.com/user-attachments/assets/9d6caa42-8638-4918-8820-eeb817307183" />
<br><br>
Также отчёт выводится в термирнале IDE (дополнительные скриншоты можно посмотреть в репозитории):
<br>
<img width="1085" height="249" alt="image" src="https://github.com/user-attachments/assets/58513b54-1298-4741-9866-b7ba59dce3f4" />


<hr><br>
<strong>Установка</strong>
<br><br>
Клонирование репозитория:<br>
<code>git clone https://github.com/your-username/your-project.git</code>
<br><br>
Переход в папку (указан относительный адрес)<br>
<code>cd Workmate_assignment</code>
<br><br>
Создание виртуального окружения:<br>
1. <code>python -m venv venv</code><br>
2. <code>source venv/bin/activate</code>  # Для Windows: <code>venv\Scripts\activate</code>
<br><br>
Установка зависимостей
<br>
<code>pip install -r requirements.txt</code>
<br><br>

<hr><br>
<strong>Использование</strong>
<br><br>
В терминале IDE, находясь в папке <code>Workmate_assignment</code> наберите:<br>
<code>python main.py --files filename_1 filename_2 ... filename_n --report report_name<br><br></code>
где:
  <ul>
    <li><code>--files</code>: имя переменной для списка файлов. Также можно использовать <code>-f</code> или <code>--filenames</code></li>
    <li><code>filename_1 filename_2 ... filename_n</code>: названия файлов. Если файлов несколько, то необходимо между названиями указывать пробел</li>
    <li><code>--report</code>: имя переменной для списка файлов. Также можно использовать <code>-r</code> или <code>--report_name</code></li>
    <li><code>report_name</code>: название для файла с отчётом. Необходимо указывать с расширением (например: perfomance.csv, report.txt и т.д.)</li>
  </ul>
<hr><br>
<strong>Структура</strong>
<br>
<img width="688" height="182" alt="image" src="https://github.com/user-attachments/assets/946997da-368e-4b92-8d09-4da2a1f76226" /><br><br>

<code>main.py</code> - скрипт, который формирует отчёт<br>
<code>main(func).py</code> - скрипт, выполняющий то же действие, но на основе функционального программирвоания (без ООП)<br>
<code>requirements.txt</code> - файл с зависимостями<br>
<code>README.md</code> - данный файл😅<br>
<br><br>

<hr><br>
<strong>Данные</strong>
<br><br>
Использованы тестовые данные от компании Workmate.<br>
Можно скачать <a href="https://drive.google.com/drive/folders/1I3BhrDAyD8SbOt168aDxjnVCacAbmnfD">здесь</a><br>

<hr><br>
<strong>Лицензия</strong>
<br><br>
Этот проект распространяется под лицензией MIT😎










  
