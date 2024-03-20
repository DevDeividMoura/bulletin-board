from datetime import datetime, timezone

# Gerar duas datas/horas no padrão ISO 8601 em UTC
data1 = datetime.now(timezone.utc).isoformat()
data2 = datetime.now(timezone.utc).isoformat()

print(data1, data2)