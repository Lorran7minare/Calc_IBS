import json, re, sys
# uso: python3 scripts/erros_acoes.py <pasta do repositório calculadora-rtc-regime-regular>
src = open(sys.argv[1] + '/src/main/java/br/gov/serpro/rtc/api/exceptionhandler/enumeration/ProblemType.java', encoding='utf-8').read()
pat = re.compile(r'\w+\(\s*\w+\.class,\s*"([^"]+)",\s*"[^"]+",\s*new CodigoErro\("([A-Z]{3}-\d{3})",\s*(null|"[^"]*"),\s*EstadoItemEnum\.(\w+)\),\s*"([^"]+)"\)', re.S)
BASE = [dict(codigo=m[1], titulo=m[0], campo=None if m[2]=='null' else m[2].strip('"'), estado=m[3], descricao=m[4]) for m in pat.findall(src)]
A = {
"REG-001": ("O item da nota veio com código de produto (NCM) e de serviço (NBS) ao mesmo tempo.", "Deixe só um: NCM se for mercadoria, NBS se for serviço. Revise o cadastro do item no sistema de vendas.", "Cadastro"),
"REG-002": ("O NCM do produto não existe na tabela oficial para a data da venda. Pode estar digitado errado ou ter sido extinto.", "Confira os 8 dígitos no cadastro. Se o NCM foi extinto, descubra o código novo (o contador ou o fornecedor do produto costumam saber) e atualize.", "Cadastro"),
"REG-003": ("O código NBS do serviço não existe na tabela oficial para a data da prestação.", "Confira o código no cadastro do serviço. A NBS foi atualizada em 2026; códigos antigos podem ter mudado.", "Cadastro"),
"REG-004": ("O CST (código de situação tributária) informado não existe para esse tributo e essa data.", "Use um CST da tabela oficial de CBS/IBS (ex.: 000, 200, 410). Peça ao contador o CST correto para o produto.", "Contador"),
"REG-005": ("O cClassTrib informado não existe ou não está vigente na data da operação.", "Confira o código de 6 dígitos na tabela oficial vigente. A tabela de cClassTrib é atualizada com frequência; atualize o sistema.", "Contador / sistema"),
"REG-006": ("O cClassTrib escolhido não combina com o CST informado. Cada cClassTrib pertence a um CST (os 3 primeiros dígitos).", "Ajuste o CST para os 3 primeiros dígitos do cClassTrib (ex.: cClassTrib 200003 usa CST 200).", "Cadastro"),
"REG-007": ("Há uma inconsistência entre o código do produto e a classificação tributária escolhida.", "Revise se o NCM/NBS está correto e se a classificação escolhida realmente se aplica a ele.", "Contador"),
"REG-008": ("A calculadora não encontrou regra de cálculo para essa classificação na data informada.", "Verifique a data da operação e se a classificação já está vigente. Se persistir, atualize a base do sistema.", "Sistema"),
"REG-009": ("Para esse CST é obrigatório informar o grupo de tributação regular, e ele não veio.", "Preencha o grupo de tributação regular no item (CST e cClassTrib da tributação regular). O sistema emissor precisa suportar esse grupo.", "Sistema"),
"REG-010": ("A classificação escolhida não pode ser usada junto com suspensão de tributo.", "Revise se o item realmente está em regime de suspensão ou se a classificação está errada.", "Contador"),
"REG-011": ("A classificação escolhida exige que o produto esteja numa lista específica da lei (ex.: cesta básica), e esse NCM não está na lista.", "Ou o produto não tem direito a esse benefício (use a regra geral ou outra classificação) ou o NCM está errado. Consulte o NCM no Classificador para ver as opções válidas.", "Contador"),
"REG-012": ("A classificação escolhida exige que o serviço esteja numa lista específica, e essa NBS não está nela.", "O serviço provavelmente não tem direito a esse tratamento. Consulte a NBS no Classificador para ver as opções válidas.", "Contador"),
"REG-013": ("O produto é tributado pelo Imposto Seletivo e os dados do IS não foram informados.", "Preencha o grupo do Imposto Seletivo no item (vale para bebidas alcoólicas, cigarros, veículos, etc., a partir de 2027).", "Sistema"),
"REG-014": ("Foram informados dados de Imposto Seletivo para um item que não tem IS.", "Remova o grupo do Imposto Seletivo desse item.", "Sistema"),
"REG-015": ("O NCM foi informado incompleto, mas esta operação exige os 8 dígitos.", "Complete o NCM com 8 dígitos no cadastro do produto.", "Cadastro"),
"REG-016": ("A NBS foi informada incompleta, mas esta operação exige o código completo (9 dígitos).", "Complete a NBS no cadastro do serviço.", "Cadastro"),
"REG-018": ("O município informado não pertence ao estado (UF) informado.", "Confira o código IBGE do município e a UF no cadastro do cliente ou da empresa.", "Cadastro"),
"REG-019": ("O código do município não existe na tabela oficial.", "Use o código IBGE de 7 dígitos do município. Confira no cadastro do cliente.", "Cadastro"),
"REG-020": ("A UF informada não existe.", "Corrija a sigla ou código da UF no cadastro.", "Cadastro"),
"REG-021": ("A data da operação (fato gerador) não foi enviada.", "Informe a data de emissão/operação. Normalmente é um problema do sistema emissor.", "Sistema"),
"REG-022": ("Foi enviado o grupo de tributação regular, mas esse CST não usa esse grupo.", "Remova o grupo de tributação regular do item.", "Sistema"),
"REG-023": ("Erro de validação genérico, sem categoria específica.", "Leia a mensagem detalhada que acompanha o erro. Se não ficar claro, encaminhe ao suporte do sistema emissor.", "Sistema"),
"REG-024": ("Algum campo tem um valor fora do formato ou das regras (ex.: texto onde deveria ser número).", "Veja qual campo foi apontado na mensagem e corrija o valor no cadastro ou na nota.", "Cadastro / sistema"),
"REG-025": ("A base de cálculo (valor sobre o qual incide o imposto) não foi informada.", "Informe o valor da base de cálculo do item. Normalmente é o valor da venda, já com descontos.", "Sistema"),
"REG-026": ("A base de CBS/IBS não bate com a soma da base do Imposto Seletivo com o próprio IS.", "Quando há IS, a base de CBS/IBS deve incluir o valor do IS. Recalcule a base.", "Sistema"),
"REG-027": ("A base de CBS/IBS ficou menor que a base do Imposto Seletivo, o que não é permitido.", "Revise os valores: a base de CBS/IBS deve ser maior ou igual à do IS.", "Sistema"),
"REG-028": ("O tipo de documento fiscal informado não existe ou não está vigente.", "Confira se o tipo de nota (NF-e, NFC-e, NFS-e etc.) está correto no sistema.", "Sistema"),
"REG-029": ("A classificação escolhida não pode ser usada nesse tipo de nota.", "Use outra classificação ou outro tipo de documento. Ex.: algumas classificações só valem em NFS-e.", "Contador"),
"REG-030": ("O NCM/NBS informado não é aceito para essa classificação nesse tipo de nota.", "Revise o código do item e a classificação escolhida para esse tipo de documento.", "Contador"),
"REG-031": ("Esse tipo de documento não aceita NCM ou NBS.", "Remova o NCM/NBS do item para esse tipo de documento.", "Sistema"),
"REG-032": ("O produto tem Imposto Seletivo, mas esse tipo de nota não aceita IS.", "Emita no tipo de documento correto para o produto (normalmente NF-e).", "Sistema"),
"REG-033": ("A classificação exige que o item tenha NCM ou NBS completo, e ele não foi informado.", "Preencha o NCM (8 dígitos) ou a NBS (9 dígitos) no item.", "Cadastro"),
"REG-034": ("A base de cálculo informada não bate com a soma dos componentes (valor, descontos, frete etc.).", "Confira os valores do item: a base precisa fechar com os componentes informados.", "Sistema"),
"REG-035": ("O produto tem Imposto Seletivo, mas a alíquota ainda não foi definida em lei e não foi informada.", "Por enquanto, informe a alíquota manualmente na simulação ou aguarde a definição legal.", "Contador"),
"REG-036": ("Foram informadas alíquotas manualmente para uma operação anterior a 2027, quando a calculadora já sabe as alíquotas.", "Para datas até 31/12/2026, não informe alíquotas: a calculadora usa CBS 0,9% e IBS 0,1% automaticamente.", "Sistema"),
"REG-037": ("Para operações a partir de 2027 é preciso informar as alíquotas (CBS, IBS estadual e municipal), que ainda não estão na base oficial.", "Informe as alíquotas estimadas na simulação. Elas serão definidas em lei e por cada estado e município.", "Sistema"),
"REG-038": ("Esse tipo de documento fiscal ainda não é tratado pela calculadora.", "Não é erro seu: aguarde atualização da calculadora oficial para esse tipo de documento.", "Aguardar Receita"),
"CAL-001": ("A calculadora não encontrou a alíquota para os dados informados.", "Confira data, UF e município. Se estiverem certos, a base de dados pode estar desatualizada.", "Sistema"),
"CAL-002": ("A alíquota padrão (de referência) não está na base para esse período.", "Comum em datas a partir de 2027, ainda sem alíquota definida. Informe as alíquotas manualmente.", "Sistema"),
"CAL-003": ("A alíquota de referência não está disponível na base.", "Verifique a data da operação e atualize a base da calculadora.", "Sistema"),
"CAL-004": ("A alíquota em valor fixo por unidade (ad rem) não foi encontrada para o produto.", "Comum em combustíveis e Imposto Seletivo. Verifique se a classificação e a unidade de medida estão corretas.", "Contador"),
"CAL-005": ("O cálculo deu alíquota negativa, sinal de parâmetros incoerentes.", "Revise reduções e ajustes informados. Se tudo estiver certo, reporte ao suporte.", "Sistema"),
"CAL-006": ("A base de dados devolveu um tipo de alíquota que o sistema não reconhece.", "Falha técnica: atualize a calculadora para a versão mais recente.", "Sistema"),
"CAL-007": ("Essa classificação ainda não foi totalmente implementada na calculadora oficial.", "Não é erro seu: aguarde a próxima versão ou calcule manualmente com o contador.", "Aguardar Receita"),
"CAL-008": ("Falha interna ao executar a fórmula de cálculo.", "Falha técnica: reporte ao suporte do sistema com o exemplo que gerou o erro.", "Sistema"),
"CAL-009": ("Não foi encontrada a regra de cálculo para essa combinação de dados.", "Confira CST, cClassTrib e data. Se estiverem certos, atualize a base.", "Sistema"),
"CAL-010": ("O percentual de redução previsto para a classificação não está na base.", "Falha da base de dados: atualize a calculadora.", "Sistema"),
"CAL-011": ("A base legal da classificação não foi encontrada.", "Falha da base de dados: atualize a calculadora.", "Sistema"),
"CAL-012": ("A combinação de tributo e CST não existe na base.", "Confira se o CST usado é de CBS/IBS ou de Imposto Seletivo, que têm tabelas diferentes.", "Contador"),
"CAL-999": ("Erro inesperado no processamento.", "Tente de novo. Se persistir, reporte ao suporte do sistema com os dados da operação.", "Sistema"),
}
base = BASE
assert set(A) == {e['codigo'] for e in base}, set(A) ^ {e['codigo'] for e in base}
for e in base:
    e['simples'], e['acao'], e['quem'] = A[e['codigo']]
base.sort(key=lambda e: (e['codigo'][:3] != 'REG', e['codigo']))
json.dump(base, open('docs/data/erros.json','w'), ensure_ascii=False, indent=1)
# markdown guide
L = ["# Guia de erros da calculadora da Reforma Tributária", "",
     "Explicação em linguagem simples dos 50 códigos de erro da Calculadora de Tributos (CBS, IBS e Imposto Seletivo), com o que fazer em cada caso.", "",
     "- **REG** = problema nos dados enviados (cadastro, nota, classificação). Quase sempre dá para resolver do seu lado.",
     "- **CAL** = falha no cálculo ou na base de dados. Normalmente é do sistema ou da própria calculadora.", ""]
for grupo, titulo in (("REG","Erros de dados (REG)"),("CAL","Erros de cálculo (CAL)")):
    L += [f"## {titulo}", ""]
    for e in base:
        if not e['codigo'].startswith(grupo): continue
        L += [f"### {e['codigo']} — {e['titulo']}", "", f"**O que significa:** {e['simples']}", "", f"**O que fazer:** {e['acao']}", "", f"**Quem resolve:** {e['quem']}" + (f" · Campo: `{e['campo']}`" if e['campo'] else ""), "",
              f"> Texto técnico oficial: {e['descricao']}", ""]
L += ["---", "Baseado no catálogo de erros da [Calculadora de Tributos — Regime Regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) (MIT, © 2026 Receita Federal do Brasil), versão 1.7.2. Material independente, sem vínculo com a Receita Federal. Não substitui orientação contábil."]
open('guia/guia-de-erros.md','w').write("\n".join(L))
print('ok', len(base))
