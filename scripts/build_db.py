# uso: python3 scripts/build_db.py <pasta do repositório calculadora-rtc-regime-regular>
# Monta calc.db aplicando as migrações Flyway oficiais em ordem.
import sqlite3, glob, os, re, sys
root = sys.argv[1]
files = glob.glob(os.path.join(root,'flyway/sql/**/*.sql'), recursive=True)
byname = {os.path.basename(f): f for f in files}
order = []
if 'beforeMigrate.sql' in byname: order.append(byname['beforeMigrate.sql'])
order.append(byname['B0001__sistema_tributario_completo.sql'])
vs = sorted([n for n in byname if n.startswith('V')], key=lambda n:int(re.match(r'V(\d+)',n).group(1)))
order += [byname[n] for n in vs]
if 'afterMigrate.sql' in byname: order.append(byname['afterMigrate.sql'])
db = sqlite3.connect('calc.db')
for f in order:
    sql = open(f, encoding='utf-8').read()
    try:
        db.executescript(sql if re.search(r"^\s*(BEGIN|COMMIT)", sql, re.M) or "foreign_keys = OFF" in sql else "BEGIN;\n"+sql+"\nCOMMIT;")
    except Exception as e:
        print('ERRO', os.path.basename(f), e)
db.commit()
print('ok', len(order))
