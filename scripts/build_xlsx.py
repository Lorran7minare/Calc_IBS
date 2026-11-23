import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule

d = json.load(open('docs/data/regras.json'))
F = 'Arial'
BLUE = Font(name=F, color='0000FF'); BLACK = Font(name=F); BOLD = Font(name=F, bold=True)
GREEN = Font(name=F, color='008000')
H = Font(name=F, bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='0F5C4A')
YEL = PatternFill('solid', fgColor='FFFF00'); INP = PatternFill('solid', fgColor='FFF9DB'); CALC = PatternFill('solid', fgColor='EEF5F1')
thin = Side(style='thin', color='D0D0D0'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical='top')
PCT = '0.00%;-0.00%;-'; BRL = '"R$" #,##0.00;[Red]-"R$" #,##0.00;-'

wb = Workbook()
# ---------- Como usar ----------
ws = wb.active; ws.title = 'Como usar'
ws.column_dimensions['A'].width = 110
linhas = [
 ('Simulador da Reforma Tributária para pequenas empresas', Font(name=F, bold=True, size=16, color='0F5C4A')),
 ('Compare quanto você paga de tributos hoje com o que vai pagar com CBS e IBS, produto por produto, e descubra o preço que mantém a sua margem.', BLACK),
 ('', BLACK),
 ('COMO USAR (3 passos)', BOLD),
 ('1. Aba "Premissas": escolha o ano que quer simular (célula amarela). Se quiser, ajuste as alíquotas estimadas.', BLACK),
 ('2. Aba "Produtos": preencha uma linha por produto ou serviço, só nas colunas de fundo amarelo-claro (A a I). As 3 primeiras linhas são exemplos: apague ou substitua.', BLACK),
 ('3. Leia o resultado nas colunas verdes (J a T): imposto novo, diferença para hoje, margem e preço sugerido.', BLACK),
 ('', BLACK),
 ('LEGENDA', BOLD),
 ('Texto azul em fundo amarelo-claro = você preenche.   Texto preto em fundo verde-claro = calculado automaticamente, não edite.   Fundo amarelo forte = premissa principal.', BLACK),
 ('', BLACK),
 ('DE ONDE TIRAR CADA DADO', BOLD),
 ('• NCM/NBS: no cadastro do produto ou na nota fiscal de compra.', BLACK),
 ('• cClassTrib: consulte o NCM/NBS no Classificador (site do projeto) ou na aba "Classificações". Ao digitar o código, a redução de alíquota é preenchida sozinha (coluna D).', BLACK),
 ('• Crédito na compra: valor de CBS + IBS destacado na nota do fornecedor, por unidade. Se o fornecedor é do Simples ou você não sabe, deixe 0.', BLACK),
 ('• PIS/Cofins e ICMS/ISS atuais: percentual sobre o preço de venda que você paga hoje. Seu contador informa. Exemplos comuns: PIS/Cofins 9,25% (lucro real) ou 3,65% (lucro presumido); ICMS 18% ou ISS 2% a 5%.', BLACK),
 ('', BLACK),
 ('O QUE A SIMULAÇÃO CONSIDERA', BOLD),
 ('• Transição oficial: 2026 é ano de teste (CBS 0,9% e IBS 0,1%, compensáveis com PIS/Cofins). Em 2027 acabam PIS/Cofins e entra a CBS cheia. De 2029 a 2032 o ICMS/ISS cai 10% por ano e o IBS sobe. Em 2033 só restam CBS e IBS.', BLACK),
 ('• O preço informado é o preço final pago pelo cliente. A CBS e o IBS são calculados "por fora" sobre esse preço.', BLACK),
 ('• As alíquotas cheias de 2027 em diante ainda não foram fixadas: os valores padrão (CBS 8,8% e IBS 17,7%, total de 26,5%) são estimativas públicas do governo e podem ser alterados na aba Premissas.', BLACK),
 ('', BLACK),
 ('LIMITAÇÕES', BOLD),
 ('• Não considera Imposto Seletivo, regimes específicos (combustíveis, financeiro, imóveis), cashback nem créditos de PIS/Cofins/ICMS que você tem hoje.', BLACK),
 ('• Empresas do Simples Nacional continuam pagando CBS/IBS dentro do DAS, a menos que optem pelo regime regular. Esta planilha simula o regime regular.', BLACK),
 ('• Simulação informativa. Não substitui o seu contador.', BLACK),
 ('', BLACK),
 (f'Reduções e classificações extraídas da Calculadora de Tributos — Regime Regular da Receita Federal (código aberto, licença MIT, © 2026 Receita Federal do Brasil), base {d["meta"]["versaoBase"][3]} de {d["meta"]["versaoBase"][1][:10]}. Ferramenta independente, sem vínculo com a Receita Federal.', Font(name=F, italic=True, color='666666')),
]
for i,(t,f) in enumerate(linhas,1):
    c = ws.cell(i,1,t); c.font=f; c.alignment=Alignment(wrap_text=True, vertical='top')

# ---------- Premissas ----------
p = wb.create_sheet('Premissas')
for col,w in zip('ABCDEFGH',(26,14,14,16,18,18,18,70)): p.column_dimensions[col].width=w
p['A1'] = 'Premissas da simulação'; p['A1'].font = Font(name=F, bold=True, size=14, color='0F5C4A')
p['A3'] = 'Ano simulado'; p['A3'].font=BOLD
p['B3'] = 2033; p['B3'].font=BLUE; p['B3'].fill=YEL; p['B3'].border=BOX
p['C3'] = 'Escolha de 2026 a 2033'; p['C3'].font=Font(name=F, italic=True, color='666666')
dv = DataValidation(type='list', formula1='"2026,2027,2028,2029,2030,2031,2032,2033"', allow_blank=False); p.add_data_validation(dv); dv.add('B3')
p['A5'] = 'Alíquota cheia da CBS'; p['B5'] = 0.088
p['A6'] = 'Alíquota cheia do IBS (UF + município)'; p['B6'] = 0.177
for c in ('B5','B6'):
    p[c].font=BLUE; p[c].fill=YEL; p[c].number_format='0.00%'; p[c].border=BOX
p['C5'] = 'Estimativa'; p['C6'] = 'Estimativa'
p['B5'].comment = Comment('Estimativa pública do Ministério da Fazenda para a alíquota de referência (total CBS+IBS ≈ 26,5%). O valor definitivo será fixado por resolução do Senado. Altere se quiser simular outro cenário.', 'Simulador')
p['B6'].comment = Comment('Estimativa pública (≈ 17,7%). Cada estado e município poderá fixar alíquota própria.', 'Simulador')
p['A7'] = 'Total estimado'; p['B7'] = '=B5+B6'; p['B7'].number_format='0.00%'; p['B7'].font=BOLD

hdr = ['Ano','CBS','IBS','CBS/IBS é pago? (1=sim)','Fração do IBS cheio','PIS/Cofins que resta','ICMS/ISS que resta','O que acontece no ano']
for j,h in enumerate(hdr,1):
    c=p.cell(9,j,h); c.font=H; c.fill=HFILL; c.alignment=Alignment(wrap_text=True, vertical='center'); c.border=BOX
anos = [
 (2026,'0.009',  '0.001', 0, None, 1, 1, 'Ano de teste: CBS 0,9% e IBS 0,1% destacados na nota, compensáveis com PIS/Cofins. Na prática não há custo extra.'),
 (2027,'=$B$5',  '0.001', 1, None, 0, 1, 'Fim de PIS/Cofins. CBS cheia. IBS simbólico de 0,1%. ICMS/ISS continuam iguais.'),
 (2028,'=$B$5',  '0.001', 1, None, 0, 1, 'Igual a 2027.'),
 (2029,'=$B$5',  None,    1, 0.1,  0, 0.9,'IBS em 10% do valor cheio; ICMS/ISS reduzidos em 10%.'),
 (2030,'=$B$5',  None,    1, 0.2,  0, 0.8,'IBS em 20%; ICMS/ISS reduzidos em 20%.'),
 (2031,'=$B$5',  None,    1, 0.3,  0, 0.7,'IBS em 30%; ICMS/ISS reduzidos em 30%.'),
 (2032,'=$B$5',  None,    1, 0.4,  0, 0.6,'IBS em 40%; ICMS/ISS reduzidos em 40%.'),
 (2033,'=$B$5',  None,    1, 1.0,  0, 0,  'Regime completo: só CBS e IBS. ICMS e ISS extintos.'),
]
for i,(a,cbs,ibs,pago,frac,pis,icms,obs) in enumerate(anos, start=10):
    p.cell(i,1,str(a)).font=BLACK
    c=p.cell(i,2); c.value = float(cbs) if not cbs.startswith('=') else cbs
    c.font = BLUE if not cbs.startswith('=') else BLACK
    c=p.cell(i,3)
    if ibs: c.value=float(ibs); c.font=BLUE
    else: c.value=f'=$B$6*E{i}'; c.font=BLACK
    p.cell(i,4,pago).font=BLUE
    c=p.cell(i,5,frac); c.font=BLUE
    p.cell(i,6,pis).font=BLUE; p.cell(i,7,icms).font=BLUE
    p.cell(i,8,obs).font=BLACK; p.cell(i,8).alignment=WRAP
    for j in (2,3,5,6,7): p.cell(i,j).number_format='0.00%'
    for j in range(1,9): p.cell(i,j).border=BOX
p['A19'] = 'Fonte do cronograma: EC 132/2023 e LC 214/2025. Valores de 2026 conforme a base oficial da calculadora da Receita (alíquotas de referência de teste).'
p['A19'].font=Font(name=F, italic=True, color='666666')

p['A21'] = 'Valores do ano simulado (usados na aba Produtos)'; p['A21'].font=BOLD
sel = [('CBS do ano','=INDEX($B$10:$B$17,MATCH(TEXT($B$3,"0"),$A$10:$A$17,0))','0.00%'),
       ('IBS do ano','=INDEX($C$10:$C$17,MATCH(TEXT($B$3,"0"),$A$10:$A$17,0))','0.00%'),
       ('CBS/IBS é pago?','=INDEX($D$10:$D$17,MATCH(TEXT($B$3,"0"),$A$10:$A$17,0))','0'),
       ('PIS/Cofins que resta','=INDEX($F$10:$F$17,MATCH(TEXT($B$3,"0"),$A$10:$A$17,0))','0%'),
       ('ICMS/ISS que resta','=INDEX($G$10:$G$17,MATCH(TEXT($B$3,"0"),$A$10:$A$17,0))','0%')]
for k,(lab,f,nf) in enumerate(sel, start=22):
    p.cell(k,1,lab).font=BLACK; c=p.cell(k,2,f); c.number_format=nf; c.font=BLACK; c.fill=CALC; c.border=BOX
p.freeze_panes='A10'

# ---------- Classificações ----------
cl = wb.create_sheet('Classificações')
cols = ['cClassTrib','Descrição','CST','Tratamento','Redução CBS','Redução IBS','Base legal (LC 214/2025)','Vigente desde']
for j,h in enumerate(cols,1):
    c=cl.cell(1,j,h); c.font=H; c.fill=HFILL; c.border=BOX
for col,w in zip('ABCDEFGH',(12,70,7,30,12,12,30,13)): cl.column_dimensions[col].width=w
rows = sorted((c for c in d['classes'].values() if c['tributo']=='CBS/IBS'), key=lambda c:c['codigo'])
for i,c in enumerate(rows, start=2):
    r=c['reducao']
    vals=[c['codigo'],c['desc'],c['cst'],c['cstDesc'],(r.get('cbs') or 0)/100,(r.get('ibsUf') or 0)/100,c['fundCurta'],c['inicio'][8:10]+'/'+c['inicio'][5:7]+'/'+c['inicio'][:4]]
    for j,v in enumerate(vals,1):
        x=cl.cell(i,j,v); x.font=BLACK
        if j in (5,6): x.number_format='0%'
    cl.cell(i,1).number_format='@'
last_cl = len(rows)+1
cl.auto_filter.ref=f'A1:H{last_cl}'; cl.freeze_panes='A2'
cl.cell(last_cl+2,1,'Fonte: tabela de cClassTrib da Calculadora de Tributos da Receita Federal (IT 2025.002 v1.71, base V0073). Algumas classificações exigem requisitos (tipo de comprador, destinação, registro).').font=Font(name=F, italic=True, color='666666')

# ---------- Produtos ----------
pr = wb.create_sheet('Produtos', 1)
heads = [
 ('Produto ou serviço','in',28),('NCM / NBS','in',13),('cClassTrib','in',11),('Redução de alíquota','calc',11),
 ('Preço final ao cliente (R$)','in',14),('Custo de compra (R$)','in',13),('Crédito CBS/IBS na compra (R$)','in',14),
 ('PIS/Cofins hoje (% do preço)','in',13),('ICMS/ISS hoje (% do preço)','in',13),
 ('Alíquota CBS+IBS efetiva','calc',12),('CBS+IBS sobre a venda (R$)','calc',13),('CBS+IBS a pagar após crédito (R$)','calc',14),
 ('Tributos antigos que restam (R$)','calc',14),('Total de tributos no ano (R$)','calc',13),('Total de tributos hoje (R$)','calc',13),
 ('Diferença (R$)','calc',12),('Margem hoje (R$)','calc',12),('Margem no ano simulado (R$)','calc',13),
 ('Preço para manter a margem (R$)','calc',14),('Ajuste de preço necessário','calc',12)]
pr['A1'] = 'Simulação por produto'; pr['A1'].font=Font(name=F, bold=True, size=14, color='0F5C4A')
pr['A2'] = '="Ano simulado: "&Premissas!B3&"   ·   CBS "&TEXT(Premissas!B22,"0.00%")&"   ·   IBS "&TEXT(Premissas!B23,"0.00%")&"   (altere na aba Premissas)"'
pr['A2'].font=GREEN
for j,(h,kind,w) in enumerate(heads,1):
    c=pr.cell(4,j,h); c.font=H; c.fill=HFILL; c.alignment=Alignment(wrap_text=True, vertical='center', horizontal='center'); c.border=BOX
    pr.column_dimensions[c.column_letter].width=w
pr.row_dimensions[4].height=58
pr['D4'].comment = Comment('Preenchida sozinha a partir do cClassTrib (aba Classificações). Sem cClassTrib = 0%.', 'Simulador')
pr['G4'].comment = Comment('CBS + IBS destacados na nota do fornecedor, por unidade. Fornecedor do Simples ou sem destaque: deixe 0.', 'Simulador')
pr['S4'].comment = Comment('Preço final que mantém a mesma margem em reais que você tem hoje, considerando os tributos do ano simulado.', 'Simulador')
exemplos = [
 ('EXEMPLO – Arroz tipo 1 (5 kg)','1006.30.21','200003',25.90,19.00,0,0.0365,0.07),
 ('EXEMPLO – Sabonete','3401.11.90','200035',4.50,2.60,0.25,0.0925,0.18),
 ('EXEMPLO – Camiseta de algodão','6109.10.00','000001',59.90,28.00,4.10,0.0365,0.18),
]
FIRST, LAST = 5, 54
for r in range(FIRST, LAST+1):
    if r-FIRST < len(exemplos):
        for j,v in enumerate(exemplos[r-FIRST],1):
            pr.cell(r,j if j<4 else j+1, v)
    pr[f'D{r}'] = f'=IF(C{r}="",0,IFERROR(INDEX(Classificações!$E$2:$E${last_cl},MATCH(TEXT(C{r},"000000"),Classificações!$A$2:$A${last_cl},0)),0))'
    g = f'IF($E{r}="","",'
    pr[f'J{r}'] = f'={g}(Premissas!$B$22+Premissas!$B$23)*(1-D{r}))'
    pr[f'K{r}'] = f'={g}E{r}-E{r}/(1+J{r}))'
    pr[f'L{r}'] = f'={g}(K{r}-N(G{r}))*Premissas!$B$24)'
    pr[f'M{r}'] = f'={g}E{r}*N(H{r})*Premissas!$B$25+E{r}*N(I{r})*Premissas!$B$26)'
    pr[f'N{r}'] = f'={g}L{r}+M{r})'
    pr[f'O{r}'] = f'={g}E{r}*(N(H{r})+N(I{r})))'
    pr[f'P{r}'] = f'={g}N{r}-O{r})'
    pr[f'Q{r}'] = f'={g}E{r}-N(F{r})-O{r})'
    pr[f'R{r}'] = f'={g}E{r}-N(F{r})-N{r})'
    pr[f'S{r}'] = (f'={g}IFERROR((Q{r}+N(F{r})-N(G{r})*Premissas!$B$24)/'
                   f'(1-Premissas!$B$24*J{r}/(1+J{r})-N(H{r})*Premissas!$B$25-N(I{r})*Premissas!$B$26),""))')
    pr[f'T{r}'] = f'={g}IFERROR(S{r}/E{r}-1,""))'
    for j in range(1,21):
        c=pr.cell(r,j); c.border=BOX
        letter=c.column_letter
        if heads[j-1][1]=='in': c.fill=INP; c.font=BLUE
        else: c.fill=CALC; c.font=BLACK
        if letter in 'BC': c.number_format='@'
        if letter in 'EFGKLMNOPQRS': c.number_format=BRL
        if letter in 'DHIJ': c.number_format='0.00%'
        if letter=='T': c.number_format='+0.0%;-0.0%;0.0%'
T = LAST+1
pr.cell(T,1,'TOTAL').font=BOLD
for L in 'KLMNOPQR':
    c=pr[f'{L}{T}']; c.value=f'=SUM({L}{FIRST}:{L}{LAST})'; c.font=BOLD; c.number_format=BRL; c.border=BOX
pr.conditional_formatting.add(f'P{FIRST}:P{LAST}', CellIsRule(operator='greaterThan', formula=['0'], font=Font(name=F, color='C00000', bold=True)))
pr.conditional_formatting.add(f'P{FIRST}:P{LAST}', CellIsRule(operator='lessThan', formula=['0'], font=Font(name=F, color='1D6B3A', bold=True)))
pr.cell(T+2,1,'Diferença positiva (vermelho) = vai pagar mais que hoje. Negativa (verde) = vai pagar menos. Valores por unidade vendida.').font=Font(name=F, italic=True, color='666666')
pr.cell(T+3,1,'Exemplos: percentuais de PIS/Cofins e ICMS são ilustrativos (lucro presumido / lucro real e ICMS interno típico). Use os da sua empresa.').font=Font(name=F, italic=True, color='666666')
pr.freeze_panes='B5'
wb.save('planilha/Simulador-Reforma-Tributaria.xlsx')
print('saved', last_cl)
