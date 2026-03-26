Atue como um Arquiteto de IA e Especialista em Salesforce DevOps.

Seu objetivo é redigir o arquivo 01_domain_boundaries.md. Este arquivo será lido de forma autônoma pelo Devin (um agente de IA de engenharia de software) toda vez que ele iniciar uma tarefa. Ele serve como o limite estrito de atuação do agente em um ecossistema Salesforce federado (múltiplos times compartilhando a mesma Org e usando Flosum para CI/CD).

Contexto da Squad (Preencha os dados):

Nome do Domínio: [Ex: Vendas / Sales Cloud]

Prefixo de Metadados do Time: [Ex: sls_ ou Sales_]

Objetos Standard Permitidos: [Ex: Opportunity, Quote, QuoteLineItem]

Objetos Standard Proibidos (De outros times): [Ex: Case, Entitlement, Invoice]

Regras que DEVEM constar obrigatoriamente no documento:

Tom: Escreva diretamente para o agente. Use imperativos fortes ("Você DEVE", "Você NÃO TEM PERMISSÃO", "É ESTritamente PROIBIDO").

Regra de Profiles vs Permission Sets: Proíba explicitamente a alteração de arquivos de Profile padrão ou compartilhados (para evitar conflitos de merge no Flosum). O agente deve SEMPRE criar ou atualizar Permission Sets com o prefixo do time.

Regra de Objetos Standard: Se o agente precisar adicionar um campo a um objeto standard não listado nos permitidos, ele deve ser instruído a pausar a tarefa e solicitar aprovação humana via chat.

Cobertura de Domínio: O agente só pode criar ou modificar Classes Apex, LWCs e Flows que comecem com o prefixo do time ou estejam dentro do diretório do pacote específico do time no formato SFDX.

Comportamento em caso de dúvida: Instrua o agente a usar a ferramenta "Ask Devin" ou interromper a execução para perguntar ao Tech Lead caso uma alteração pareça cruzar a fronteira do domínio.

Gere o conteúdo do arquivo em formato Markdown (.md), otimizado para RAG (Retrieval-Augmented Generation) e leitura agentiva.