# Guia de erros da calculadora da Reforma Tributária

Explicação em linguagem simples dos 50 códigos de erro da Calculadora de Tributos (CBS, IBS e Imposto Seletivo), com o que fazer em cada caso.

- **REG** = problema nos dados enviados (cadastro, nota, classificação). Quase sempre dá para resolver do seu lado.
- **CAL** = falha no cálculo ou na base de dados. Normalmente é do sistema ou da própria calculadora.

## Erros de dados (REG)

### REG-001 — NCM e NBS informadas simultaneamente

**O que significa:** O item da nota veio com código de produto (NCM) e de serviço (NBS) ao mesmo tempo.

**O que fazer:** Deixe só um: NCM se for mercadoria, NBS se for serviço. Revise o cadastro do item no sistema de vendas.

**Quem resolve:** Cadastro

> Texto técnico oficial: Apenas uma nomenclatura (NCM ou NBS) deve ser informada por item. A presença simultânea impede a classificação.

### REG-002 — NCM não encontrada

**O que significa:** O NCM do produto não existe na tabela oficial para a data da venda. Pode estar digitado errado ou ter sido extinto.

**O que fazer:** Confira os 8 dígitos no cadastro. Se o NCM foi extinto, descubra o código novo (o contador ou o fornecedor do produto costumam saber) e atualize.

**Quem resolve:** Cadastro · Campo: `ncm`

> Texto técnico oficial: O código NCM informado não foi localizado na base de nomenclaturas vigente para a data do fato gerador.

### REG-003 — NBS não encontrada

**O que significa:** O código NBS do serviço não existe na tabela oficial para a data da prestação.

**O que fazer:** Confira o código no cadastro do serviço. A NBS foi atualizada em 2026; códigos antigos podem ter mudado.

**Quem resolve:** Cadastro · Campo: `nbs`

> Texto técnico oficial: O código NBS informado não foi localizado na base de nomenclaturas vigente para a data do fato gerador.

### REG-004 — Situação tributária não encontrada

**O que significa:** O CST (código de situação tributária) informado não existe para esse tributo e essa data.

**O que fazer:** Use um CST da tabela oficial de CBS/IBS (ex.: 000, 200, 410). Peça ao contador o CST correto para o produto.

**Quem resolve:** Contador · Campo: `cst`

> Texto técnico oficial: A situação tributária (CST) informada não existe na base de dados para o tributo e data do fato gerador.

### REG-005 — Classificação tributária não encontrada

**O que significa:** O cClassTrib informado não existe ou não está vigente na data da operação.

**O que fazer:** Confira o código de 6 dígitos na tabela oficial vigente. A tabela de cClassTrib é atualizada com frequência; atualize o sistema.

**Quem resolve:** Contador / sistema · Campo: `cClassTrib`

> Texto técnico oficial: A classificação tributária informada não foi localizada na base vigente para a data do fato gerador.

### REG-006 — Classificação tributária não vinculada à situação tributária

**O que significa:** O cClassTrib escolhido não combina com o CST informado. Cada cClassTrib pertence a um CST (os 3 primeiros dígitos).

**O que fazer:** Ajuste o CST para os 3 primeiros dígitos do cClassTrib (ex.: cClassTrib 200003 usa CST 200).

**Quem resolve:** Cadastro · Campo: `cClassTrib`

> Texto técnico oficial: A classificação tributária informada não está vinculada à situação tributária selecionada.

### REG-007 — Erro de nomenclatura

**O que significa:** Há uma inconsistência entre o código do produto e a classificação tributária escolhida.

**O que fazer:** Revise se o NCM/NBS está correto e se a classificação escolhida realmente se aplica a ele.

**Quem resolve:** Contador · Campo: `ncm`

> Texto técnico oficial: A nomenclatura informada apresenta inconsistência com as regras de classificação tributária vigentes.

### REG-008 — Tratamento de classificação não encontrado

**O que significa:** A calculadora não encontrou regra de cálculo para essa classificação na data informada.

**O que fazer:** Verifique a data da operação e se a classificação já está vigente. Se persistir, atualize a base do sistema.

**Quem resolve:** Sistema · Campo: `cClassTrib`

> Texto técnico oficial: Não foi encontrado tratamento de classificação tributária para os parâmetros informados.

### REG-009 — Grupo de tributação regular não informado

**O que significa:** Para esse CST é obrigatório informar o grupo de tributação regular, e ele não veio.

**O que fazer:** Preencha o grupo de tributação regular no item (CST e cClassTrib da tributação regular). O sistema emissor precisa suportar esse grupo.

**Quem resolve:** Sistema · Campo: `tributacaoRegular`

> Texto técnico oficial: O grupo de tributação regular é obrigatório para a situação tributária selecionada e não foi informado.

### REG-010 — Incompatibilidade com suspensão

**O que significa:** A classificação escolhida não pode ser usada junto com suspensão de tributo.

**O que fazer:** Revise se o item realmente está em regime de suspensão ou se a classificação está errada.

**Quem resolve:** Contador · Campo: `tributacaoRegular/cClassTrib`

> Texto técnico oficial: A classificação tributária informada é incompatível com a situação de suspensão aplicada ao item.

### REG-011 — NCM não vinculada

**O que significa:** A classificação escolhida exige que o produto esteja numa lista específica da lei (ex.: cesta básica), e esse NCM não está na lista.

**O que fazer:** Ou o produto não tem direito a esse benefício (use a regra geral ou outra classificação) ou o NCM está errado. Consulte o NCM no Classificador para ver as opções válidas.

**Quem resolve:** Contador · Campo: `ncm`

> Texto técnico oficial: O código NCM informado não está vinculado a nenhuma classificação tributária vigente.

### REG-012 — NBS não vinculada

**O que significa:** A classificação escolhida exige que o serviço esteja numa lista específica, e essa NBS não está nela.

**O que fazer:** O serviço provavelmente não tem direito a esse tratamento. Consulte a NBS no Classificador para ver as opções válidas.

**Quem resolve:** Contador · Campo: `nbs`

> Texto técnico oficial: O código NBS informado não está vinculado a nenhuma classificação tributária vigente.

### REG-013 — Dados do Imposto Seletivo não informados

**O que significa:** O produto é tributado pelo Imposto Seletivo e os dados do IS não foram informados.

**O que fazer:** Preencha o grupo do Imposto Seletivo no item (vale para bebidas alcoólicas, cigarros, veículos, etc., a partir de 2027).

**Quem resolve:** Sistema · Campo: `impostoSeletivo`

> Texto técnico oficial: Os dados do Imposto Seletivo são obrigatórios para a classificação tributária selecionada e não foram informados.

### REG-014 — Dados do Imposto Seletivo informados indevidamente

**O que significa:** Foram informados dados de Imposto Seletivo para um item que não tem IS.

**O que fazer:** Remova o grupo do Imposto Seletivo desse item.

**Quem resolve:** Sistema · Campo: `impostoSeletivo`

> Texto técnico oficial: Os dados do Imposto Seletivo foram informados, mas a classificação tributária selecionada não prevê incidência.

### REG-015 — NCM completo não informado

**O que significa:** O NCM foi informado incompleto, mas esta operação exige os 8 dígitos.

**O que fazer:** Complete o NCM com 8 dígitos no cadastro do produto.

**Quem resolve:** Cadastro · Campo: `ncm`

> Texto técnico oficial: O código NCM deve ser informado com todos os dígitos (completo) para a operação solicitada.

### REG-016 — NBS completo não informado

**O que significa:** A NBS foi informada incompleta, mas esta operação exige o código completo (9 dígitos).

**O que fazer:** Complete a NBS no cadastro do serviço.

**Quem resolve:** Cadastro · Campo: `nbs`

> Texto técnico oficial: O código NBS deve ser informado com todos os dígitos (completo) para a operação solicitada.

### REG-018 — Município não pertencente à UF

**O que significa:** O município informado não pertence ao estado (UF) informado.

**O que fazer:** Confira o código IBGE do município e a UF no cadastro do cliente ou da empresa.

**Quem resolve:** Cadastro

> Texto técnico oficial: O município informado não pertence à UF indicada na operação.

### REG-019 — Município não encontrado

**O que significa:** O código do município não existe na tabela oficial.

**O que fazer:** Use o código IBGE de 7 dígitos do município. Confira no cadastro do cliente.

**Quem resolve:** Cadastro

> Texto técnico oficial: O código do município informado não foi localizado na base de dados.

### REG-020 — UF não encontrada

**O que significa:** A UF informada não existe.

**O que fazer:** Corrija a sigla ou código da UF no cadastro.

**Quem resolve:** Cadastro

> Texto técnico oficial: A UF informada para a operação não foi encontrada na base de dados.

### REG-021 — Data do fato gerador não informada

**O que significa:** A data da operação (fato gerador) não foi enviada.

**O que fazer:** Informe a data de emissão/operação. Normalmente é um problema do sistema emissor.

**Quem resolve:** Sistema

> Texto técnico oficial: A data do fato gerador é obrigatória e não foi informada na requisição.

### REG-022 — Grupo de tributação regular informado indevidamente

**O que significa:** Foi enviado o grupo de tributação regular, mas esse CST não usa esse grupo.

**O que fazer:** Remova o grupo de tributação regular do item.

**Quem resolve:** Sistema · Campo: `tributacaoRegular`

> Texto técnico oficial: O grupo de tributação regular foi informado, mas a situação tributária selecionada não o exige.

### REG-023 — Erro genérico de validação

**O que significa:** Erro de validação genérico, sem categoria específica.

**O que fazer:** Leia a mensagem detalhada que acompanha o erro. Se não ficar claro, encaminhe ao suporte do sistema emissor.

**Quem resolve:** Sistema

> Texto técnico oficial: Erro de validação que não se enquadra em nenhuma categoria específica.

### REG-024 — Campo inválido

**O que significa:** Algum campo tem um valor fora do formato ou das regras (ex.: texto onde deveria ser número).

**O que fazer:** Veja qual campo foi apontado na mensagem e corrija o valor no cadastro ou na nota.

**Quem resolve:** Cadastro / sistema

> Texto técnico oficial: O valor informado para o campo não é válido conforme as regras de negócio.

### REG-025 — Base de cálculo não informada

**O que significa:** A base de cálculo (valor sobre o qual incide o imposto) não foi informada.

**O que fazer:** Informe o valor da base de cálculo do item. Normalmente é o valor da venda, já com descontos.

**Quem resolve:** Sistema · Campo: `baseCalculo`

> Texto técnico oficial: A base de cálculo de CBS e IBS é obrigatória quando o grupo do Imposto Seletivo não é informado.

### REG-026 — Base de cálculo inconsistente

**O que significa:** A base de CBS/IBS não bate com a soma da base do Imposto Seletivo com o próprio IS.

**O que fazer:** Quando há IS, a base de CBS/IBS deve incluir o valor do IS. Recalcule a base.

**Quem resolve:** Sistema · Campo: `baseCalculo`

> Texto técnico oficial: A base de cálculo de CBS e IBS informada difere da soma da base de cálculo do Imposto Seletivo com o Imposto Seletivo informado.

### REG-027 — Base de cálculo menor que a base de cálculo do Imposto Seletivo

**O que significa:** A base de CBS/IBS ficou menor que a base do Imposto Seletivo, o que não é permitido.

**O que fazer:** Revise os valores: a base de CBS/IBS deve ser maior ou igual à do IS.

**Quem resolve:** Sistema · Campo: `baseCalculo`

> Texto técnico oficial: A base de cálculo de CBS e IBS informada é menor que a base de cálculo do Imposto Seletivo.

### REG-028 — Tipo de documento fiscal não encontrado

**O que significa:** O tipo de documento fiscal informado não existe ou não está vigente.

**O que fazer:** Confira se o tipo de nota (NF-e, NFC-e, NFS-e etc.) está correto no sistema.

**Quem resolve:** Sistema · Campo: `tpDoc`

> Texto técnico oficial: O tipo de documento fiscal (tpDoc) informado na operação não existe ou está fora de vigência na data do fato gerador.

### REG-029 — Classificação tributária não vinculada ao tipo de documento

**O que significa:** A classificação escolhida não pode ser usada nesse tipo de nota.

**O que fazer:** Use outra classificação ou outro tipo de documento. Ex.: algumas classificações só valem em NFS-e.

**Quem resolve:** Contador · Campo: `cClassTrib`

> Texto técnico oficial: A classificação tributária informada não possui vínculo vigente com o tipo de documento fiscal (tpDoc) da operação.

### REG-030 — Nomenclatura incompatível com o tipo de documento

**O que significa:** O NCM/NBS informado não é aceito para essa classificação nesse tipo de nota.

**O que fazer:** Revise o código do item e a classificação escolhida para esse tipo de documento.

**Quem resolve:** Contador

> Texto técnico oficial: A nomenclatura informada (NCM ou NBS) não é aceita para a classificação tributária no tipo de documento fiscal (tpDoc) da operação.

### REG-031 — Nomenclatura não permitida para o tipo de documento

**O que significa:** Esse tipo de documento não aceita NCM ou NBS.

**O que fazer:** Remova o NCM/NBS do item para esse tipo de documento.

**Quem resolve:** Sistema

> Texto técnico oficial: O tipo de documento fiscal (tpDoc) da operação não admite o preenchimento de NCM ou NBS.

### REG-032 — Imposto Seletivo não admitido pelo tipo de documento

**O que significa:** O produto tem Imposto Seletivo, mas esse tipo de nota não aceita IS.

**O que fazer:** Emita no tipo de documento correto para o produto (normalmente NF-e).

**Quem resolve:** Sistema · Campo: `impostoSeletivo`

> Texto técnico oficial: O NCM/NBS informado é tributado pelo Imposto Seletivo, mas o tipo de documento fiscal (tpDoc) da operação não admite Imposto Seletivo.

### REG-033 — Nomenclatura obrigatória não informada

**O que significa:** A classificação exige que o item tenha NCM ou NBS completo, e ele não foi informado.

**O que fazer:** Preencha o NCM (8 dígitos) ou a NBS (9 dígitos) no item.

**Quem resolve:** Cadastro

> Texto técnico oficial: A classificação tributária possui anexo com NCM e NBS aplicáveis e exige o preenchimento de um deles, completo, para o tipo de documento fiscal (tpDoc) da operação.

### REG-034 — Base de cálculo inconsistente

**O que significa:** A base de cálculo informada não bate com a soma dos componentes (valor, descontos, frete etc.).

**O que fazer:** Confira os valores do item: a base precisa fechar com os componentes informados.

**Quem resolve:** Sistema · Campo: `baseCalculo`

> Texto técnico oficial: A base de cálculo declarada no item diverge da base calculada a partir dos componentes informados

### REG-035 — Alíquota do Imposto Seletivo não informada

**O que significa:** O produto tem Imposto Seletivo, mas a alíquota ainda não foi definida em lei e não foi informada.

**O que fazer:** Por enquanto, informe a alíquota manualmente na simulação ou aguarde a definição legal.

**Quem resolve:** Contador · Campo: `aliquotasNominais/impostoSeletivo`

> Texto técnico oficial: A NCM/NBS possui incidência do Imposto Seletivo, mas a alíquota ainda não foi definida em lei e não foi informada pelo usuário.

### REG-036 — Alíquotas nominais informadas indevidamente

**O que significa:** Foram informadas alíquotas manualmente para uma operação anterior a 2027, quando a calculadora já sabe as alíquotas.

**O que fazer:** Para datas até 31/12/2026, não informe alíquotas: a calculadora usa CBS 0,9% e IBS 0,1% automaticamente.

**Quem resolve:** Sistema · Campo: `aliquotasNominais`

> Texto técnico oficial: As alíquotas nominais não podem ser informadas para fato gerador anterior a 01/01/2027, pois a calculadora resolve as alíquotas vigentes.

### REG-037 — Alíquotas nominais não informadas

**O que significa:** Para operações a partir de 2027 é preciso informar as alíquotas (CBS, IBS estadual e municipal), que ainda não estão na base oficial.

**O que fazer:** Informe as alíquotas estimadas na simulação. Elas serão definidas em lei e por cada estado e município.

**Quem resolve:** Sistema · Campo: `aliquotasNominais`

> Texto técnico oficial: As alíquotas nominais (cbs, ibsEstadual e ibsMunicipal) devem ser informadas para fato gerador a partir de 01/01/2027.

### REG-038 — Tipo de documento fiscal não tratado

**O que significa:** Esse tipo de documento fiscal ainda não é tratado pela calculadora.

**O que fazer:** Não é erro seu: aguarde atualização da calculadora oficial para esse tipo de documento.

**Quem resolve:** Aguardar Receita · Campo: `tpDoc`

> Texto técnico oficial: O tipo de documento fiscal (tpDoc) informado na operação não possui tratamento implementado na calculadora.

## Erros de cálculo (CAL)

### CAL-001 — Alíquota não encontrada

**O que significa:** A calculadora não encontrou a alíquota para os dados informados.

**O que fazer:** Confira data, UF e município. Se estiverem certos, a base de dados pode estar desatualizada.

**Quem resolve:** Sistema

> Texto técnico oficial: Não foi possível localizar a alíquota aplicável para os parâmetros tributários informados.

### CAL-002 — Alíquota padrão não encontrada

**O que significa:** A alíquota padrão (de referência) não está na base para esse período.

**O que fazer:** Comum em datas a partir de 2027, ainda sem alíquota definida. Informe as alíquotas manualmente.

**Quem resolve:** Sistema

> Texto técnico oficial: A alíquota padrão (de referência) não foi encontrada na base para o tributo e período informados.

### CAL-003 — Alíquota de referência não encontrada

**O que significa:** A alíquota de referência não está disponível na base.

**O que fazer:** Verifique a data da operação e atualize a base da calculadora.

**Quem resolve:** Sistema

> Texto técnico oficial: A alíquota de referência necessária para o cálculo não está disponível na base de dados.

### CAL-004 — Alíquota ad rem não encontrada

**O que significa:** A alíquota em valor fixo por unidade (ad rem) não foi encontrada para o produto.

**O que fazer:** Comum em combustíveis e Imposto Seletivo. Verifique se a classificação e a unidade de medida estão corretas.

**Quem resolve:** Contador

> Texto técnico oficial: A alíquota ad rem (valor fixo por unidade) não foi localizada para o produto e período informados.

### CAL-005 — Alíquota negativa

**O que significa:** O cálculo deu alíquota negativa, sinal de parâmetros incoerentes.

**O que fazer:** Revise reduções e ajustes informados. Se tudo estiver certo, reporte ao suporte.

**Quem resolve:** Sistema

> Texto técnico oficial: O cálculo resultou em uma alíquota negativa, o que indica inconsistência nos parâmetros tributários.

### CAL-006 — Tipo de alíquota desconhecido

**O que significa:** A base de dados devolveu um tipo de alíquota que o sistema não reconhece.

**O que fazer:** Falha técnica: atualize a calculadora para a versão mais recente.

**Quem resolve:** Sistema

> Texto técnico oficial: O tipo de alíquota retornado pela base de dados não é reconhecido pelo sistema.

### CAL-007 — Classificação tributária em desenvolvimento

**O que significa:** Essa classificação ainda não foi totalmente implementada na calculadora oficial.

**O que fazer:** Não é erro seu: aguarde a próxima versão ou calcule manualmente com o contador.

**Quem resolve:** Aguardar Receita · Campo: `cClassTrib`

> Texto técnico oficial: A classificação tributária informada ainda não possui implementação completa no sistema.

### CAL-008 — Erro no avaliador de expressão aritmética

**O que significa:** Falha interna ao executar a fórmula de cálculo.

**O que fazer:** Falha técnica: reporte ao suporte do sistema com o exemplo que gerou o erro.

**Quem resolve:** Sistema

> Texto técnico oficial: Ocorreu um erro ao avaliar a expressão aritmética utilizada no cálculo do tributo.

### CAL-009 — Tratamento tributário não encontrado

**O que significa:** Não foi encontrada a regra de cálculo para essa combinação de dados.

**O que fazer:** Confira CST, cClassTrib e data. Se estiverem certos, atualize a base.

**Quem resolve:** Sistema

> Texto técnico oficial: O tratamento tributário aplicável não foi localizado para a combinação de parâmetros informada.

### CAL-010 — Percentual de redução não encontrado

**O que significa:** O percentual de redução previsto para a classificação não está na base.

**O que fazer:** Falha da base de dados: atualize a calculadora.

**Quem resolve:** Sistema

> Texto técnico oficial: O percentual de redução de alíquota previsto para a classificação não foi encontrado na base.

### CAL-011 — Fundamentação não encontrada

**O que significa:** A base legal da classificação não foi encontrada.

**O que fazer:** Falha da base de dados: atualize a calculadora.

**Quem resolve:** Sistema

> Texto técnico oficial: A fundamentação legal para a classificação tributária não foi localizada na base de dados.

### CAL-012 — Tributo/situação tributária não encontrado

**O que significa:** A combinação de tributo e CST não existe na base.

**O que fazer:** Confira se o CST usado é de CBS/IBS ou de Imposto Seletivo, que têm tabelas diferentes.

**Quem resolve:** Contador

> Texto técnico oficial: A combinação de tributo e situação tributária informada não foi localizada na base.

### CAL-999 — Erro interno do sistema

**O que significa:** Erro inesperado no processamento.

**O que fazer:** Tente de novo. Se persistir, reporte ao suporte do sistema com os dados da operação.

**Quem resolve:** Sistema

> Texto técnico oficial: Erro interno inesperado durante o processamento do cálculo. Contate o suporte se o problema persistir.

---
Baseado no catálogo de erros da [Calculadora de Tributos — Regime Regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) (MIT, © 2026 Receita Federal do Brasil), versão 1.7.2. Material independente, sem vínculo com a Receita Federal. Não substitui orientação contábil.