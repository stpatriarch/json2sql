from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("json2sql")
except PackageNotFoundError:
    __version__ = "\"_\""


__title__ = "json2sql"
__description__ = "Convert json file to sql db."
__url__ = "https://github.com/stpatriarch/json2sql"

__author__ = "stpatriarch"
__author_email__ = "chinaryannarek@gmail.com"
__license__ = "MIT"

