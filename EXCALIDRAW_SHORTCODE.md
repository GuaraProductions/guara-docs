# Excalidraw SVG Shortcode - Documentação

Este repositório contém um shortcode Hugo para embutir diagramas Excalidraw com funcionalidade interativa de zoom e pan.

## Funcionalidades

- ✨ **Zoom interativo** - Use a roda do mouse ou pinça em dispositivos móveis
- 🖱️ **Pan/Arrastar** - Clique e arraste para navegar por diagramas grandes
- 📱 **Suporte mobile** - Totalmente responsivo com gestos touch
- ⚡ **Performance estática** - Zero dependências externas, JavaScript vanilla
- 🎨 **Controles visuais** - Botões de zoom in, zoom out e reset
- ♿ **Acessível** - Suporte a leitores de tela e navegação por teclado

## Estrutura do Projeto

```
guara-help-site/
├── .github/
│   └── workflows/
│       └── excalidraw-to-svg.yml    # Converte .excalidraw para .svg
├── content/
│   └── example.md                    # Exemplo de uso
├── layouts/
│   ├── _default/
│   │   ├── baseof.html              # Template base
│   │   └── single.html              # Template de página
│   └── shortcodes/
│       └── excalidraw.html          # Shortcode principal
├── static/
│   ├── diagrams/
│   │   └── example.svg              # Exemplo de diagrama
│   └── js/
│       └── excalidraw-pan-zoom.js   # Biblioteca de zoom/pan
└── hugo.toml                         # Configuração Hugo
```

## Instalação

### Pré-requisitos

- Hugo (versão 0.100.0 ou superior)
- Node.js (para o workflow de conversão de Excalidraw)

### Setup

1. Clone o repositório:
```bash
git clone https://github.com/GuaraProductions/guara-help-site.git
cd guara-help-site
```

2. Execute o servidor Hugo localmente:
```bash
hugo server -D
```

3. Acesse http://localhost:1313 no navegador

## Uso do Shortcode

### Sintaxe Básica

```markdown
{{</* excalidraw src="diagrams/my-diagram.svg" alt="Meu Diagrama" */>}}
```

### Parâmetros

| Parâmetro | Obrigatório | Padrão | Descrição |
|-----------|-------------|--------|-----------|
| `src` | Sim | - | Caminho para o arquivo SVG relativo a `static/` |
| `alt` | Não | "Excalidraw Diagram" | Texto alternativo para acessibilidade |
| `width` | Não | "100%" | Largura do container |
| `height` | Não | "600px" | Altura do container |

### Exemplos

#### Exemplo básico
```markdown
{{</* excalidraw src="diagrams/architecture.svg" alt="Arquitetura do Sistema" */>}}
```

#### Com tamanho personalizado
```markdown
{{</* excalidraw src="diagrams/flowchart.svg" alt="Fluxograma" width="800px" height="500px" */>}}
```

#### Diagrama em tela cheia
```markdown
{{</* excalidraw src="diagrams/large-diagram.svg" alt="Diagrama Completo" width="100%" height="800px" */>}}
```

## Workflow de Conversão Excalidraw

O repositório inclui um GitHub Actions workflow que automaticamente converte arquivos `.excalidraw` em `.svg`.

### Como Funciona

1. Crie seus diagramas em [Excalidraw](https://excalidraw.com/)
2. Exporte como arquivo `.excalidraw`
3. Adicione o arquivo na pasta `static/diagrams/` ou qualquer subpasta
4. Faça commit e push do arquivo
5. O GitHub Actions automaticamente:
   - Detecta o arquivo `.excalidraw`
   - Converte para `.svg`
   - Faz commit do arquivo SVG resultante

### Estrutura de Arquivos Recomendada

```
static/
└── diagrams/
    ├── architecture.excalidraw
    ├── architecture.svg         # Gerado automaticamente
    ├── flowchart.excalidraw
    └── flowchart.svg            # Gerado automaticamente
```

## Recursos Técnicos

### Interatividade

- **Zoom com mouse wheel**: Role para cima/baixo
- **Pan com mouse**: Clique e arraste
- **Zoom com touch**: Pinça com dois dedos
- **Pan com touch**: Arraste com um dedo
- **Botões de controle**:
  - `+` - Aumentar zoom
  - `-` - Diminuir zoom
  - Reset - Voltar ao estado inicial

### Performance

- Zero dependências externas (não usa bibliotecas de terceiros)
- JavaScript vanilla otimizado
- Carregamento lazy de SVGs
- Suporte para diagramas muito grandes
- Transformações CSS3 para melhor performance

### Compatibilidade

- ✅ Chrome/Edge (últimas versões)
- ✅ Firefox (últimas versões)
- ✅ Safari (últimas versões)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Desenvolvimento

### Testando Localmente

```bash
# Iniciar servidor de desenvolvimento
hugo server -D

# Build para produção
hugo --minify
```

### Adicionando Novos Diagramas

1. Crie o diagrama em Excalidraw
2. Salve como `.excalidraw` em `static/diagrams/`
3. Commit e push
4. Aguarde o workflow converter para SVG
5. Use o shortcode em suas páginas

### Personalizando Estilos

O shortcode usa estilos inline para máxima portabilidade, mas você pode adicionar CSS customizado:

```css
/* Personalizar container */
.excalidraw-container {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Personalizar botões */
.excalidraw-controls button {
  background: #f3f4f6;
}

.excalidraw-controls button:hover {
  background: #e5e7eb;
}
```

## Solução de Problemas

### O SVG não aparece

- Verifique se o caminho em `src` está correto
- Confirme que o arquivo SVG existe em `static/diagrams/`
- Verifique o console do navegador para erros

### Zoom/Pan não funciona

- Certifique-se de que `excalidraw-pan-zoom.js` está carregado
- Verifique se há erros JavaScript no console
- Tente recarregar a página

### GitHub Actions não converte arquivos

- Verifique se o arquivo tem extensão `.excalidraw`
- Confirme que o workflow está habilitado
- Veja os logs do workflow em Actions

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Suporte

Para reportar bugs ou sugerir melhorias, abra uma issue no GitHub.
