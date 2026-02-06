# Guara Docs

Um site estático para ajudar desenvolvedores no Godot, construído com Hugo e hospedado no GitHub Pages.

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

## 🧩 Adicionar ao Hub

Para adicionar um projeto na lista do hub:

1. Crie um arquivo Markdown em [content/hub](content/hub) usando como base o archetype [archetypes/resources.md](archetypes/resources.md).
2. Preencha os campos obrigatorios do front matter (titulo, descricao, categoria, genero, versao do Godot e link externo).
3. Salve o arquivo com um nome curto e descritivo (slug), por exemplo: `meu-projeto.md`.

Exemplo minimo:

```md
---
title: "Meu Projeto"
date: 2026-02-06
draft: false
external_link: "https://exemplo.com"
godot_version: ["4"]
genre: ["2D"]
category: ["Games"]
description: "Descricao curta do projeto."
build:
	render: "never"
	list: "always"
---
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 💡 Suporte

Para reportar bugs ou sugerir melhorias, abra uma [issue](https://github.com/GuaraProductions/guara-docs/issues).

## 🙏 Creditos

A versao inicial da lista curada foi baseada na lista do projeto [awesome-godot](https://github.com/godotengine/awesome-godot) (licenca CC-BY-4.0).
