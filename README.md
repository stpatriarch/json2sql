# json2sql

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<br>

Այս պարզագույն գործքը կոչված է օգնել կատարելու վերափոխում(convert) **json** ֆայլը **sql** ֆայլի։ Այն ընդունում է **\*.json** և վերափոխում այն **\*.db-ի։**

## Տեղադրումը

```bash
# հավելվածի պատճենում
git clone https://github.com/stpatriarch/json2sql.git
cd json2sql

# վիրտուալ աշխատավայրի ստեղծում և ակտիվացում
python3 -m venv venv
source venv/bin/activate

# գործիքի տեղադրում
pip install .
```

### Կիրառությունը

```bash

json2sql -i input_file.json -t sql_table_name
```

## Supported Database Engines

SQL | STATUS | DATE
---- | ---- | ----
**SqLite** | $${\color{green}Ավարտված}$$ | 03.09.25
**PosgreSql** | $${\color{red}Պլանավորված}$$ | -
**MySql** | $${\color{red}Պլանավորված}$$ | -
