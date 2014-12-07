from rango.models import Dict 
from rango.forms import DictForm
import csv

with open('dict_db.csv', 'rb') as file:
    reader = csv.reader(file, delimiter = ',')
    for row in reader:
        created = Dict.objects.get_or_create(
            text = row[0]
            translation = row[1]
        )
