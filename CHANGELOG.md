# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não Publicado]

### Adicionado
- Implementação inicial do projeto com carregamento de arquivos e extração de informações.
- DAO base e DAO de identidade.
- Lógica de pré-processamento de texto com tokenização e limpeza.
- Extração de informações nomeadas com análise de relações.
- Crawler para busca e download de PDFs públicos.
- Armazenamento estruturado em banco de dados.
- Interface simples de execução.
- Pipeline completo de processamento de documentos.
- README com descrição do projeto.
- Script para segmentação de documentos por página.
- Salvamento de execuções e gerenciamento de versões de documentos.

### Corrigido
- Ajuste de path do banco de dados.
- Correção na substituição de caracteres especiais e regex quebrando entidades.
- Fix para nome de atributos e problemas com RG e CPF.
- Correção de lógica ao deletar documentos inexistentes.
- Validações para garantir consistência no pipeline.
- Truncamento de texto excessivo para evitar exceções.

### Refatorado
- Reestruturação de modelos e separação de responsabilidades.
- Alterações nas DAOs e manipulação de entidades.
- Mover lógica de quebra de página para pré-processamento.
- Eliminação de prints e código obsoleto.



