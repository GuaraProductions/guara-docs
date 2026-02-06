# Guara Docs

A static site to help Godot developers, built with Hugo and hosted on GitHub Pages.

### Prerequisites

- Hugo 0.100.0 or later
- Node.js (for Excalidraw conversion)

### Installation

```bash
# Clone the repository
git clone https://github.com/GuaraProductions/guara-docs.git
cd guara-docs

# Run the development server
hugo server -D
```

Open http://localhost:1313

## 🚀 Deploy

The site is automatically deployed to GitHub Pages on pushes to the `main` branch. The deployment workflow:

1. Installs Hugo (version 0.128.0 extended)
2. Builds the site with optimizations (`--gc --minify`)
3. Deploys to GitHub Pages

**Site URL**: https://guaraproductions.github.io/guara-docs/

To deploy manually:
1. Go to Actions on GitHub
2. Select the workflow "Deploy Hugo site to Pages"
3. Click "Run workflow"

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/MyFeature`)
3. Commit your changes (`git commit -m 'Add: My feature'`)
4. Push to the branch (`git push origin feature/MyFeature`)
5. Open a Pull Request

## 🧩 Add to the Hub

To add a project to the hub list:

1. Create a Markdown file in [content/hub](content/hub) using the archetype [archetypes/resources.md](archetypes/resources.md) as a base.
2. Fill in the required front matter fields (title, description, category, genre, Godot version, and external link).
3. Save the file with a short, descriptive name (slug), for example: `my-project.md`.

Minimal example:

```md
---
title: "My Project"
date: 2026-02-06
draft: false
external_link: "https://example.com"
godot_version: ["4"]
genre: ["2D"]
category: ["Games"]
description: "Short description of the project."
build:
	render: "never"
	list: "always"
---
```

## 📄 License

This project is licensed under the MIT license. See [LICENSE](LICENSE) for details.

## 💡 Support

To report bugs or suggest improvements, open an [issue](https://github.com/GuaraProductions/guara-docs/issues).

## 🙏 Credits

The initial version of the curated list was based on the [awesome-godot](https://github.com/godotengine/awesome-godot) list (CC-BY-4.0 license).
