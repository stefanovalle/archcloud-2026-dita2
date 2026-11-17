# Lab 7 · la funzione rossi-salva-telemetria (Python 3.12)
# Riceve il messaggio dalla regola di IoT Core e lo scrive nella tabella.
# Cambiate TABELLA con il vostro cognome, poi Deploy.
import json, boto3
from decimal import Decimal

TABELLA = "rossi-telemetria"
tab = boto3.resource("dynamodb").Table(TABELLA)

def lambda_handler(event, context):
    # DynamoDB non accetta i numeri con la virgola di Python: li convertiamo in Decimal
    item = json.loads(json.dumps(event), parse_float=Decimal)
    tab.put_item(Item=item)
    return {"ok": True}
