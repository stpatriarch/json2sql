## Install and Use

---


### Installing

```sh
# Repository cloning.
git clone https://github.com/stpatriarch/json2sql.git && cd json2sql

# Virtula environment create a activation.
python3 -m venv venv && source venv/bin/activate

# installing.
pip install .
```

### Usage

```bash
# input_file.json ->  json file path  sql_table_name -> sql table name
json2sql -i input_file.json -t sql_table_name
```
