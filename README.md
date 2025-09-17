# json2sql

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<br>

### :toolbox: json ֆայլերի փոխակերպիչ sql *.db ֆայլի մեկ հրամանով։

Այս պարզագույն գործիքը կոչված է օգնել կատարելու վերափոխում ( **convert** ) **json** ֆայլը **sql** ֆայլի։ Այն ընդունում է **\*.json** և վերափոխում այն **\*.db-ի։**

**Տեղադրման և շահագործման գործընթացը** [ասյտեղ](docs/INSTALL_AM.md)

#### :pushpin: Նպատակը։

Շատ հաճախ հավելվածների համար բազզա ստեղծելիս, կազմում էի տվյալները json ֆորմատով այն ավելի հարմար է, դյուրակազմ է և հեշտությամբ է խմբագրվում, սակայն հետագայում դրա վերափոխումը արդեն հիմնական տվյալերի բազզայի մեջ պահանջում է հավելյալ սկրիպտի ստեղծմանը և թեսթավորմանը, դա խլում է բավական ժամանակ։ Այս նպատակին է ծառայում այն գործիքը, այն մասսամբ լուծում է այդ խնդիրը։

---

#### :bulb: Հնարավորություններ։

Գործիքը աշխատում է բոլոր, *հիմնական տարածում գտած json ֆայլերի հետ*։ Գործիքը վերլուծում է տրված json ֆայլի կառուցվածքը, եթե անհրաժեշտություն կա մինիմալ փոփոխություն մցնում դրանց կառուցվածքի մեջ, այսպես եթե json ֆայլը պարունակում է տվյալի տեսակ որը, ՏԲ շարժիչը չի սատարում ծրագիրը կվերափոխի այդ հատվածը ընդունելի ֆորմատի։ (օրինակ՝ sqlite չունի համապատսխան տվյալ array-ի համար, եթե json-ում առկա է այդպիսի հատված գործիքը կվերափոխվի՝ string ֆորմատի)։

Այնուհետ ստեղծվում է json ֆայլին համանուն բազզա, ստեղծվում է տրված անունով աղյուսակ, ֆորմատովորումը կատարվում է առկա համապատասխան բանալի արժեքների անուններով և դրանց տվյալ արժեքներին համապատսպախան տվյալների տեսակների համաձայն։

Վերջում կատարվում է փոխակերպում, այսինքն json ֆայլից տվյլաները գրանցվում են ստեղծված աղյուակում։

---

#### :paperclip: Շահագործում։

Տեղադրումից հետո գործիքը ընդունում է երկու պարտադիր պարամետր աշխատանքը հաջողությամբ ավարտելու համար։

* `-i կամ --input` - մուտքային json ֆայլի ուղղին։
* `-t կամ --table` - ստեղծյալ աղյուակի անունը։
* `json2sql -i input_file.json -t sql_table_name` - ամբողջական հրամանի տեսքը։

**Ընդունելի  json -> sql.db օրինակները տես՝**[ այստեղ](docs/REFERANCES.md)

---

#### :triangular_flag_on_post: Պրոեկտի կարգավիճակը։

Պրոկետը դեռ գնտվում է իր կառուցման փուլում ներքևի աղյուակում նշված են այժմ սատավող և պլանավորված Տվյլաների Բազզաների պլանավորված և ավարտին հասցված շարժիչների կարգավիճակները։

SQL | STATUS | DATE | MARK |
---- | ---- | ---- | ---- |
**SqLite** | Ավարտված | 03.09.25 |  :white_check_mark: |
**PosgreSql** | Պլանավորված | - | :large_blue_diamond: |
**MySql** | Պլանավորված | - | :large_blue_diamond: |

---

## 🇷🇺

### :toolbox: Конвертер JSON-файлов в SQL \*.db одним действием.

Этот простой инструмент предназначен для того, чтобы выполнить преобразование (**convert**) **JSON**-файла в **SQL**-файл. Он принимает **\*.json** и преобразует его в **\*.db**.

**Процесс установки и использования** [здесь](docs/INSTALL_RU.md).

#### :pushpin: Цель

Очень часто при создании базы данных для удобства данные составляются в формате JSON — он более удобный, лёгкий для понимания и редактирования. Но позже преобразование этих данных в основную базу требует создания дополнительных скриптов и тестирования, что отнимает немало времени. Этот инструмент и предназначен для частичного решения этой проблемы.

---

#### :bulb: Возможности

Инструмент работает со всеми *основными распространёнными форматами JSON*. Он анализирует структуру входного файла и при необходимости вносит минимальные изменения. Например, если JSON содержит тип данных, который СУБД не поддерживает, программа преобразует его в допустимый формат (например, массив в строку, так как SQLite не имеет отдельного типа для массивов).

Затем создаётся база с тем же именем, что и у JSON-файла, создаётся таблица с указанным именем, а структура таблицы формируется на основе ключей и их типов значений.

В конце происходит импорт — данные из JSON-файла вставляются в созданную таблицу.

---

#### :paperclip: Использование

После установки инструмент принимает два обязательных параметра:

* `-i или --input` — путь к входному JSON-файлу.
* `-t или --table` — имя создаваемой таблицы.
* `json2sql -i input_file.json -t sql_table_name` - Пример команды.

**Примеры допустимых преобразований json → sql.db смотри [здесь](docs/REFERANCES.md).**

---

#### :triangular_flag_on_post: Статус проекта

Проект всё ещё находится в стадии разработки. Ниже приведена таблица с поддерживаемыми и планируемыми СУБД:

 SQL | СТАТУС | ДАТА | МЕТКА |
 ---- | ---- | -------- | ---- |
 **SqLite**     | Завершено   | 03.09.25 | :white_check_mark:   |
 **PostgreSql** | Планируется | –        | :large_blue_diamond: |
 **MySql**      | Планируется | –        | :large_blue_diamond: |

---

## 🇬🇧

### :toolbox: Convert JSON files into SQL \*.db with a single command.

This simple tool is designed to perform a transformation (**convert**) from a **JSON** file into an **SQL** file. It takes **\*.json** and converts it into **\*.db**.

**Installation and usage guide** [here](docs/INSTALL_EN.md).

#### :pushpin: Purpose

When creating databases for applications, data is often prepared in JSON format — it’s more convenient, lightweight, and easy to edit. However, later converting this into the main database usually requires writing additional scripts and testing, which consumes a lot of time. This tool is made to partially solve that issue.

---

#### :bulb: Features

The tool works with all *commonly used JSON formats*. It analyzes the given JSON file’s structure and, if necessary, applies minimal adjustments. For example, if the JSON file contains a data type unsupported by the SQL engine, the tool will transform it into an acceptable format (e.g., converting arrays into strings, since SQLite doesn’t support arrays as a native type).

After that, a database with the same name as the JSON file is created, along with a table under the given name. The table’s structure is generated based on the keys and their value types.

Finally, the transformation is executed — meaning that data from the JSON file is inserted into the newly created table.

---

#### :paperclip: Usage

After installation, the tool requires two mandatory parameters to run successfully:

* `-i or --input` — path to the input JSON file.
* `-t or --table` — name of the table to be created.
*  `json2sql -i input_file.json -t sql_table_name` - Example full command.

**See acceptable json → sql.db examples [here](docs/REFERANCES.md).**

---

#### :triangular_flag_on_post: Project status

The project is still under development. The following table shows currently supported and planned database engines:

 SQL | STATUS | DATE | MARK |
 -------------- | ---- | ---- | ---- |
 **SqLite**     | Completed | 03.09.25 | :white_check_mark:   |
 **PostgreSql** | Planned   | –        | :large_blue_diamond: |
 **MySql**      | Planned   | –        | :large_blue_diamond: |

---
