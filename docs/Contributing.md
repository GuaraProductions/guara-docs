# Godot Project Classification Reference

This document outlines the allowed values for categorizing Godot engine projects, including versioning, game genres, and functional categories.

---

## 1. Godot Versions (godot_version)

These values specify the compatibility or nature of the project's integration with the Godot engine.

- **4** — Projects specifically for Godot 4.x (GDExtension).
- **3** — Projects specifically for Godot 3.x (GDNative).
- **2** — Projects for Godot 2.x.
- **both** — Compatible with both Godot 3 and 4.
- **module** — Engine-level C++ modules.
- **gdnative** — Projects using the Godot 3 GDNative interface.
- **gde** — Projects using the Godot 4 GDExtension interface.
- **unknown** — Use when the specific version cannot be determined.

---

## 2. Genres (genre)

Standard genres used to describe gameplay mechanics for games, demos, and templates.

- **Perspective**
  - 2D, 3D, Isometric, Top-down, Side-scroller
- **Action / Combat**
  - Action, Shooter, FPS, TPS, Platformer, Puzzle-platformer, Roguelike, Metroidvania
- **Strategy / RPG**
  - RPG, Strategy, RTS, Turn-based, Simulation
- **Casual / Other**
  - Puzzle, Racing, Sports, Adventure, Casual, Party, Sandbox, Narrative, Music/Rhythm
- **Social / Environment**
  - Multiplayer, Singleplayer, Co-op, Educational, VR, AR

---

## 3. Categories (category)

Functional classifications to define what the repository or project provides.

### Core Content
- **Games** — Full playable games.
- **Demos** — Small technical demonstrations.
- **Templates** — Boilerplate projects for starting new games.
- **Projects** — Large-scale applications or complex repositories.

### Extension & Tooling
- **Plugins and scripts** — GDScript/C# addons or individual scripts.
- **Modules** — C++ engine modules.
- **Tools** — External or internal utility software.
- **Editor integrations** — Enhancements for the Godot editor.
- **Importer/Exporter** — Tools for handling external file formats.

### Development & Assets
- **Assets** — Art, sound, or 3D model collections.
- **Themes** — UI themes or editor color/syntax schemes.
- **GDScript/C# editor support** — External IDE support (VSCode, Vim, etc.).
- **CI/CD / Automation** — Scripts for build pipelines, GitHub Actions, Docker.

### Specialized
- **Networking** — Tools specifically for online connectivity.
- **Audio / Physics / UI / Localization** — Specialized functional libraries.
- **Testing / Performance** — QA and optimization tools.
- **Bash scripts** — Shell utilities and helpers.
- **Other / Contents / Examples** — General utility and organizational tags.