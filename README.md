# Guara Docs

Um site estático para ajudar desenvolvedores no Godot, construído com Hugo e hospedado no GitHub Pages.

## 🎨 Recursos

- ✨ **Diagramas Excalidraw Interativos** - Shortcode Hugo com zoom e pan para diagramas complexos
- ⚡ **Performance Estática** - JavaScript vanilla, sem dependências externas
- 🚀 **Conversão Automática** - GitHub Actions converte `.excalidraw` para `.svg` automaticamente
- 📱 **Mobile-friendly** - Suporte total a gestos touch (pinça e arrastar)
- ♿ **Acessível** - Compatível com leitores de tela

## 🚀 Quick Start

### Pré-requisitos

- Hugo 0.100.0 ou superior
- Node.js (para conversão de Excalidraw)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/GuaraProductions/guara-docs.git
cd guara-docs

# Execute o servidor de desenvolvimento
hugo server -D
```

Acesse http://localhost:1313

## 📖 Uso do Shortcode Excalidraw

### Sintaxe Básica

```markdown
{{</* excalidraw src="diagrams/my-diagram.svg" alt="Meu Diagrama" */>}}
```

### Parâmetros

- `src` (obrigatório) - Caminho para o arquivo SVG relativo a `static/`
- `alt` (opcional) - Texto alternativo para acessibilidade
- `width` (opcional) - Largura do container (padrão: 100%)
- `height` (opcional) - Altura do container (padrão: 600px)

### Exemplo Completo

```markdown
{{</* excalidraw src="diagrams/architecture.svg" alt="Arquitetura do Sistema" width="800px" height="600px" */>}}
```

## 🎯 Funcionalidades Interativas

- **Zoom com roda do mouse** - Role para aumentar/diminuir
- **Pan com mouse** - Clique e arraste para mover
- **Zoom touch** - Pinça com dois dedos em dispositivos móveis
- **Pan touch** - Arraste com um dedo
- **Controles visuais** - Botões de zoom in, zoom out e reset

## 📁 Estrutura do Projeto

```
guara-docs/
├── .github/workflows/       # GitHub Actions (deploy automático)
├── content/                 # Conteúdo do site
├── layouts/                 # Templates Hugo
│   └── shortcodes/         # Shortcode Excalidraw
├── static/                  # Arquivos estáticos
│   ├── diagrams/           # Diagramas SVG
│   └── js/                 # JavaScript
└── hugo.toml               # Configuração Hugo
```

## 🚀 Deploy

O site é automaticamente deployado no GitHub Pages quando há push na branch `main`. O workflow de deploy:

1. Instala o Hugo (versão 0.128.0 extended)
2. Faz build do site com otimizações (`--gc --minify`)
3. Faz deploy no GitHub Pages

**URL do site**: https://guaraproductions.github.io/guara-docs/

Para fazer deploy manual:
1. Vá em Actions no GitHub
2. Selecione o workflow "Deploy Hugo site to Pages"
3. Clique em "Run workflow"
   
## 🤝 Contribuindo

Contribuições são bem-vindas! Veja como:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Minha feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 💡 Suporte

Para reportar bugs ou sugerir melhorias, abra uma [issue](https://github.com/GuaraProductions/guara-docs/issues).
