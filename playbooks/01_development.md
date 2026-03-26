# Playbook: Desenvolvimento e Testes Locais (Salesforce DX)

**Objetivo:** Este playbook define o procedimento operacional padrão (SOP) que você, Devin, deve seguir para implementar, testar e validar qualquer alteração de código ou metadado no ecossistema Salesforce antes de iniciar a orquestração com o Flosum.

**Pré-requisitos Obrigatórios:**
- Você já executou `scripts/01_setup_env.sh` (Ferramental instalado).
- Você já executou `scripts/02_auth_orgs.sh` (Autenticado na Org de QA/DevHub).
- Você leu `knowledge-base/01_domain_boundaries.md` e sabe quais metadados pode alterar.

---

## FASE 1: Preparação do Ambiente Efêmero (Scratch Org)

Como trabalhamos em um modelo modular e seguro, você não desenvolverá diretamente na Org compartilhada. Você usará uma Scratch Org.
Utilize a Agent Skill importada do repositório `sf-skills` para criar o ambiente.

1. **Criar Scratch Org:** Invoque a skill apropriada (ex: `@skills:create-scratch-org`) ou execute:
   `sf org create scratch -f config/project-scratch-def.json -a devin-scratch -d -y 1`
2. **Deploy Inicial (Push):**
   Envie o código base atual para a Scratch Org:
   `sf project deploy start --target-org devin-scratch`
3. **Injeção de Dados (Se aplicável):**
   Se houver dados de teste em `data-seeding/export.json`, popule a Scratch Org usando o SFDMU:
   `sf sfdmu run --sourceusername csvfile --targetusername devin-scratch -p data-seeding/sfdmu/`

---

## FASE 2: Desenvolvimento da Funcionalidade

Ao codificar Classes Apex, LWC ou Triggers, apoie-se nas Agent Skills do `Jaganpro/sf-skills` para acelerar a criação de esqueletos estruturais e manter o padrão.

1. **Criação de Arquivos:** Se precisar criar uma nova classe ou componente, use as skills (ex: `@skills:create-apex-class` ou `@skills:create-lwc`).
2. **Respeito aos Limites:** Nunca modifique objetos padrão (ex: `Account`) se isso for proibido no seu `domain_boundaries.md`.
3. **Rastreamento de Mudanças:** Como a Scratch Org possui *Source Tracking*, faça as alterações e garanta que elas estejam sincronizadas com o seu workspace local:
   `sf project retrieve start --target-org devin-scratch`

---

## FASE 3: Testes Locais e Garantia de Qualidade (DoD)

Você não tem permissão para abrir um Pull Request se o código não passar nesta fase. O Flosum rejeitará o pacote posteriormente se a cobertura for baixa ou se houver falhas de segurança.

**Passo 3.1: Testes Unitários Apex**
Execute a suite de testes localmente na Scratch Org. Nossa meta de cobertura de código é **estritamente superior a 85%**.
- Use a skill do repositório: `@skills:run-apex-tests` 
- *Fallback (CLI):* `sf apex run test --target-org devin-scratch --code-coverage --result-format human --wait 10`
- **Regra de Auto-Correção:** Se a cobertura for menor que 85% ou testes falharem, **não peça ajuda ao humano**. Analise o log de erro, corrija a classe de teste, faça o deploy novamente e re-execute a suite.

**Passo 3.2: Análise Estática (Salesforce Code Analyzer)**
Não injete dívida técnica. Verifique vulnerabilidades (Injeção SOQL, FLS, problemas de PMD).
- Use a skill correspondente (ex: `@skills:run-sfdx-scanner`) ou execute:
  `sf scanner run --target force-app --engine pmd,eslint --severity-threshold 3 --format table`
- **Regra de Auto-Correção:** Se o scanner retornar severidade 1, 2 ou 3, você deve refatorar o código para corrigir o apontamento antes de prosseguir.

---

## FASE 4: Sincronização Final e Git

1. **Validação do Delta:** Certifique-se de que nenhum arquivo indesejado (como Profiles de outros domínios) foi acidentalmente modificado ou baixado. Verifique seu `git status`.
2. **Commit Estruturado:**
   Faça o commit das alterações com uma mensagem descritiva (ex: `feat(sales-core): adiciona calculo de margem na Quote`).
3. **Próximo Passo:**
   Agora que o desenvolvimento e os testes locais estão concluídos, leia o playbook `playbooks/03_flosum_integration.md` para validar seu pacote contra a Org de QA via Flosum CLI antes de abrir o Pull Request.