---
title: "Exemplo de Diagrama Excalidraw"
date: 2026-01-27
draft: false
---

# Exemplo de Uso do Shortcode Excalidraw

Este é um exemplo de como usar o shortcode Excalidraw para embutir diagramas SVG com funcionalidade de zoom e pan.

## Uso Básico

Para usar o shortcode, basta adicionar:

```
{{</* excalidraw src="diagrams/example.svg" alt="Exemplo de Diagrama" */>}}
```

## Exemplo ao Vivo

Abaixo está um diagrama Excalidraw com interatividade completa:

{{< excalidraw src="diagrams/example.svg" alt="Exemplo de Diagrama" >}}

## Recursos

- **Zoom com roda do mouse**: Role a roda do mouse para aumentar ou diminuir o zoom
- **Pan/Arrastar**: Clique e arraste para mover o diagrama
- **Botões de controle**: Use os botões no canto superior direito para:
  - Zoom in (+)
  - Zoom out (-)
  - Reset (voltar ao estado inicial)
- **Suporte a touch**: Em dispositivos móveis, use pinça para zoom e arraste com um dedo para pan

## Parâmetros Opcionais

Você pode personalizar o tamanho do container:

```
{{</* excalidraw src="diagrams/example.svg" alt="Meu Diagrama" width="800px" height="500px" */>}}
```

### Parâmetros disponíveis:

- `src` (obrigatório): Caminho para o arquivo SVG relativo à pasta `static/`
- `alt` (opcional): Texto alternativo para acessibilidade
- `width` (opcional): Largura do container (padrão: 100%)
- `height` (opcional): Altura do container (padrão: 600px)
