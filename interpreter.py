import datetime

from babel.dates import format_date
from quantulum3 import parser
import dateparser

def pretty(sentence):
    quantum = parser.parse(sentence)[0]
    return f"{quantum.value.real}{quantum.unit.symbols[0]}"


sm = "3.50 GB left"
used = "used (12%)"
qtyused = "513 MB"
days_past = "days elapsed (32%)"

print(f"{pretty(sm)} restant")
print(f"{pretty(qtyused)} utilisé ({pretty(used)})")
print(f"{pretty(days_past)} jours passés")


bill_date = "Bill date: August 13, 2022"
bill_date = bill_date[len("Bill date: "):]
dt = dateparser.parse(bill_date)
today = datetime.datetime.now()
diff = dt - today
print(diff.days + 1)
print(dateparser.parse(bill_date))
print(format_date(dt, locale='fr'))
