# Kit Reforma Tributária para pequenas empresas

Três produtos feitos a partir dos dados oficiais da [Calculadora de Tributos — Regime Regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) da Receita Federal (base V0073, de 09/11/2026):

| # | Produto | Onde está | Para quem |
|---|---|---|---|
| 1 | **Classificador**: o usuário digita o NCM ou a NBS e vê se tem redução, isenção ou Imposto Seletivo, em linguagem simples, com uma simulação rápida de preço | `docs/index.html` | Dono de pequena empresa, comerciante, prestador de serviço |
| 3 | **Planilha simuladora**: compara os tributos de hoje com CBS/IBS por produto e ano (2026 a 2033) e calcula o preço que mantém a margem | `planilha/Simulador-Reforma-Tributaria.xlsx` | Pequenas empresas no regime regular, ou avaliando sair do Simples |
| 4 | **Guia de erros**: os 50 códigos de erro da calculadora (REG/CAL) explicados, com o que fazer e quem resolve | `docs/erros.html` (versão web) e `guia/guia-de-erros.md` (base para e-book) | Quem emite nota e começa a receber rejeição |

## Como testar

**Online (GitHub Pages):** em *Settings → Pages*, escolha *Deploy from a branch*, branch `main`, pasta `/docs`. O site fica em `https://<seu-usuario>.github.io/<repositorio>/`.
> Em repositório **privado**, o GitHub Pages só funciona em plano pago. Para testar de graça, deixe o repositório público ou rode localmente.

**No seu computador:**

```bash
cd docs
python3 -m http.server 8000
# abra http://localhost:8000
```

Abrir o `index.html` direto (dois cliques) não funciona: o navegador bloqueia o carregamento dos dados.

**Planilha:** abra no Excel, LibreOffice ou Google Sheets. Comece pela aba *Como usar*.

## Como atualizar quando a Receita publicar uma nova versão

```bash
git clone --depth 1 https://github.com/ReceitaFederal/calculadora-rtc-regime-regular /tmp/rtc
python3 scripts/build_db.py /tmp/rtc        # monta o banco a partir das migrações oficiais
python3 scripts/extract.py                  # gera docs/data/*.json
python3 scripts/erros_acoes.py /tmp/rtc     # gera docs/data/erros.json e guia/guia-de-erros.md
python3 scripts/build_xlsx.py               # regera a planilha (precisa de openpyxl)
```

Se a Receita criar códigos de erro novos, o `erros_acoes.py` acusa e é preciso escrever a explicação deles no dicionário `A`.

## Limitações conhecidas

- O classificador mostra os tratamentos **ligados ao NCM/NBS**. Tratamentos que dependem do tipo de operação (exportação, venda ao governo, doação) aparecem só na aba *Todas as classificações*.
- Vários benefícios exigem requisitos que a ferramenta não verifica (quem compra, destinação, registro em órgão).
- As alíquotas cheias de 2027 em diante ainda não foram fixadas. A planilha e o simulador usam estimativas editáveis (CBS 8,8% e IBS 17,7%).
- A planilha não considera Imposto Seletivo, regimes específicos nem créditos de PIS/Cofins/ICMS de hoje.

## Licença e aviso

Ferramenta independente, **sem vínculo com a Receita Federal**, e não substitui a orientação de um contador. Não use o nome ou o logotipo da Receita na divulgação.

Os dados vêm de software publicado pela Receita Federal sob licença MIT. O aviso de copyright original está em [`NOTICE-RECEITA-FEDERAL.txt`](NOTICE-RECEITA-FEDERAL.txt) e deve acompanhar qualquer redistribuição.
