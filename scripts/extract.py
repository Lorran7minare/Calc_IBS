# uso: python3 scripts/extract.py  (lê calc.db, gera docs/data/*.json)
import sqlite3, json, re, sys
import datetime
HOJE = datetime.date.today().isoformat()  # vigência considerada
db = sqlite3.connect('calc.db')
def vig(fim): return fim is None or fim[:10] >= HOJE
def clean(t):
    if t is None: return ''
    t = re.sub(r'<[^>]+>', '', t.replace('\\n', ' '))
    return re.sub(r'\s+', ' ', t).strip()

# NCM full descriptions
ncm_all = {c: (d, f) for c, d, i, f in db.execute('select * from NCM')}
def ncm_desc(code):
    parts = []
    for L in (4, 5, 6, 7, 8):
        p = code[:L]
        if p in ncm_all and vig(ncm_all[p][1]):
            d = clean(ncm_all[p][0]).lstrip('- ').strip()
            if d and (not parts or d != parts[-1]): parts.append(d)
    return ' › '.join(parts)
ncm = {c: ncm_desc(c) for c, (d, f) in ncm_all.items() if len(c) == 8 and vig(f)}

nbs_all = {c: (d, f) for c, d, lc, i, f in db.execute('select * from NBS')}
def nbs_desc(code):
    parts = []
    for L in (3, 5, 6, 7, 8, 9):
        p = code[:L]
        if p in nbs_all and vig(nbs_all[p][1]):
            d = clean(nbs_all[p][0])
            if d and (not parts or d != parts[-1]): parts.append(d)
    return ' › '.join(parts)
nbs = {c: nbs_desc(c) for c, (d, f) in nbs_all.items() if len(c) == 9 and vig(f)}

is_sitr = {r[0] for r in db.execute('select TRST_SITR_ID from TRIBUTO_SITUACAO_TRIBUTARIA where TRST_TBTO_ID=1')} - {r[0] for r in db.execute('select TRST_SITR_ID from TRIBUTO_SITUACAO_TRIBUTARIA where TRST_TBTO_ID<>1')}
sit = {i: (cd, d) for i, cd, d, *_ in db.execute('select SITR_ID,SITR_CD,SITR_DESCRICAO,SITR_FIM_VIGENCIA from SITUACAO_TRIBUTARIA')}

classes = {}
id2cd = {}
rows = db.execute('''select CLTR_ID,CLTR_CD,CLTR_DESCRICAO,CLTR_SITR_ID,CLTR_TIPO_ALIQUOTA,CLTR_NOMENCLATURA,
  CLTR_INICIO_VIGENCIA,CLTR_FIM_VIGENCIA,CLTR_IN_APROPRIACAO_CREDITOS_ADQUIRENTES_CBS,CLTR_CREDITO_OPERACAO_ANTECEDENTE
  from CLASSIFICACAO_TRIBUTARIA order by CLTR_INICIO_VIGENCIA''').fetchall()
for (cid, cd, desc, sitr, tipo, nomen, ini, fim, cred, antec) in rows:
    cd = ('IS-' + cd) if sitr in is_sitr else cd
    id2cd[cid] = cd
    if not vig(fim): continue
    red = {}
    for tb, val, f in db.execute('select PERE_TBTO_ID,PERE_VALOR,PERE_FIM_VIGENCIA from PERCENTUAL_REDUCAO where PERE_CLTR_ID=?', (cid,)):
        if vig(f): red[{2:'cbs',3:'ibsUf',4:'ibsMun'}[tb]] = val
    fund = [(clean(c), clean(t)) for c, t, f in db.execute('''select l.FDLG_TEXTO_CURTO,l.FDLG_TEXTO,fc.FDCL_FIM_VIGENCIA from FUNDAMENTACAO_CLASSIFICACAO fc
        join FUNDAMENTACAO_LEGAL l on l.FDLG_ID=fc.FDCL_FDLG_ID where fc.FDCL_CLTR_ID=?''', (cid,)) if vig(f)]
    aliqfix = [(tb, v) for tb, v, f in db.execute('select AADV_TBTO_ID,AADV_VALOR,AADV_FIM_VIGENCIA from ALIQUOTA_AD_VALOREM where AADV_CLTR_ID=?', (cid,)) if vig(f) and v is not None]
    classes[cd] = dict(tributo='IS' if cd.startswith('IS-') else 'CBS/IBS', codigo=cd.replace('IS-',''), desc=clean(desc), cst=sit[sitr][0], cstDesc=sit[sitr][1], tipo=tipo, nomenclatura=nomen,
        inicio=ini[:10], fim=fim[:10] if fim else None, reducao=red,
        creditoAdquirente=bool(cred), creditoAnterior=antec,
        fundCurta='; '.join(dict.fromkeys(f[0] for f in fund if f[0])), fundTexto=' | '.join(dict.fromkeys(f[1] for f in fund if f[1]))[:1500],
        aliqFixa={ {2:'cbs',3:'ibsUf',4:'ibsMun'}.get(tb,'is'): v for tb, v in aliqfix})

anexo = {i: (n, it, clean(t)) for i, n, it, t in db.execute('select ANXO_ID,ANXO_NUMERO,ANXO_NUMERO_ITEM,ANXO_TEXTO_ITEM from ANEXO')}
exc = {}
for nc, nid, f in db.execute('select ENCM_NCM_CD,ENCM_NCMA_ID,ENCM_FIM_VIGENCIA from EXCECAO_NCM_APLICAVEL'):
    if vig(f): exc.setdefault(nid, []).append(nc)
def rules(table, pre, has_exc):
    out = []
    for rid, code, cid, aid, f in db.execute(f'select {pre}_ID,{pre}_{"NCM" if pre=="NCMA" else "NBS"}_CD,{pre}_CLTR_ID,{pre}_ANXO_ID,{pre}_FIM_VIGENCIA from {table}'):
        if not vig(f): continue
        cd = id2cd.get(cid)
        if cd not in classes: continue
        a = anexo.get(aid)
        out.append([code, cd, f'Anexo {a[0]}, item {a[1]}: {a[2]}' if a else '', exc.get(rid, []) if has_exc else []])
    return out
data = dict(
    meta=dict(versaoBase=db.execute('select * from VERSAO_BASE_DADO order by 1 desc limit 1').fetchone(), geradoEm=HOJE,
              aliquotaReferencia2026=dict(cbs=0.9, ibsUf=0.1, ibsMun=0.0)),
    classes=classes, regrasNcm=rules('NCM_APLICAVEL','NCMA',True), regrasNbs=rules('NBS_APLICAVEL','NBSA',False))
json.dump(data, open('docs/data/regras.json','w'), ensure_ascii=False, separators=(',',':'))
json.dump(ncm, open('docs/data/ncm.json','w'), ensure_ascii=False, separators=(',',':'))
json.dump(nbs, open('docs/data/nbs.json','w'), ensure_ascii=False, separators=(',',':'))
print(len(ncm), len(nbs), len(classes), len(data['regrasNcm']), len(data['regrasNbs']))
