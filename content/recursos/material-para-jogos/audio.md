---
title: "Áudio"
date: 2026-01-30T12:15:42-03:00
draft: false
---

Atenção: lembre-se sempre de conferir as licenças de qualquer efeito sonoro ou música que você encontrar na internet. No desenvolvimento de jogos, a escolha do formato de áudio correto é vital para equilibrar o uso de memória RAM e o tamanho do instalador final.

## Formatos

### WAV (.wav)
Formato de áudio sem compressão (PCM), o que garante a máxima fidelidade sonora possível.
* **Vantagens:** Baixíssimo uso de processador para ser reproduzido, pois não precisa ser "descompactado".
* **Uso:** Ideal para efeitos sonoros curtos (SFX), como sons de passos, tiros ou interface (UI), que são tocados repetidamente.

### Ogg Vorbis (.ogg)
Um formato de compressão com perda de dados, similar ao MP3, porém de código aberto e mais eficiente para loops.
* **Vantagens:** Permite arquivos longos com tamanhos muito pequenos. É o formato preferencial da Godot para trilhas sonoras.
* **Uso:** O padrão para músicas de fundo (BGM) e trilhas de ambiente, especialmente se precisarem de um loop perfeito.

### MP3 (.mp3)
O formato de compressão mais popular do mundo. Embora amplamente suportado, pode apresentar pequenos problemas em loops contínuos devido ao silêncio inserido no início/fim do arquivo pelo codec.
* **Vantagens:** Alta compatibilidade e boa compressão para áudios longos.
* **Uso:** Trilhas sonoras ou narrações longas onde o "loop perfeito" não seja uma prioridade absoluta.

---

## Onde encontrar assets de Áudio

### 1. Kenney (Audio)
Oferece pacotes temáticos de alta qualidade que cobrem as necessidades básicas de quase qualquer protótipo ou jogo comercial.
* **Licença:** CC0 (Domínio Público).
* **Destaque:** Conjuntos de sons de interface, cassino, ficção científica e vozes narradas.
* **Link:** [kenney.nl/assets/category:Audio](https://kenney.nl/assets/category:Audio)

### 2. Soniss (GDC Bundles)
Anualmente, a Soniss disponibiliza pacotes gigantescos de áudio profissional de alta definição (Foley) extraídos de bibliotecas pagas.
* **Licença:** Royalty-Free (Uso comercial permitido).
* **Destaque:** Qualidade de cinema para sons de ambiente, armas e veículos.
* **Link:** [sonniss.com/gameaudiogdc](https://sonniss.com/gameaudiogdc/)

### 3. Freesound.org
Uma plataforma colaborativa imensa onde usuários do mundo todo compartilham gravações de campo e efeitos sonoros experimentais.
* **Destaque:** Sistema de busca por tags muito eficiente para sons específicos e orgânicos.
* **Link:** [freesound.org](https://freesound.org/)

### 4. Incompetech (Kevin MacLeod)
O site mais famoso para encontrar músicas de fundo para jogos e vídeos. Permite filtrar por gênero, humor e ritmo.
* **Licença:** Geralmente CC-BY (Requer atribuição).
* **Destaque:** Trilhas instrumentais variadas que se encaixam em diversos contextos.
* **Link:** [incompetech.com/music/](https://incompetech.com/music/royalty-free/music.html)

---

## Tabela Comparativa de Licenças (Áudio)

| Site | Licença Padrão | Precisa de Créditos? | Uso Comercial? |
| :--- | :--- | :--- | :--- |
| **Kenney** | CC0 | Não | Sim |
| **Soniss** | Royalty-Free | Não | Sim |
| **Freesound** | Varia (CC0, CC-BY) | Depende da licença | Sim |
| **Incompetech** | CC-BY | Sim | Sim |
