---
title: "Audio"
date: 2026-01-30T12:15:42-03:00
draft: false
---

Attention: always remember to check the licenses of any sound effect or music you find on the internet. In game development, choosing the correct audio format is vital to balance RAM usage and the final installer size.

## Formats

### WAV (.wav)
Uncompressed audio format (PCM), which ensures the maximum possible sound fidelity.
* **Advantages:** Very low CPU usage for playback since it doesn't need to be "decompressed."
* **Usage:** Ideal for short sound effects (SFX), such as footsteps, gunshots, or interface (UI) sounds, which are played repeatedly.

### Ogg Vorbis (.ogg)
A lossy compression format, similar to MP3, but open-source and more efficient for loops.
* **Advantages:** Allows for long files with very small sizes. It is Godot's preferred format for soundtracks.
* **Usage:** The standard for background music (BGM) and ambient tracks, especially if they require a seamless loop.

### MP3 (.mp3)
The world's most popular compression format. Although widely supported, it may present minor issues in continuous loops due to the silence inserted at the beginning/end of the file by the codec.
* **Advantages:** High compatibility and good compression for long audio files.
* **Usage:** Soundtracks or long narrations where a "perfect loop" is not an absolute priority.

---

## Where to find Audio assets

### 1. Kenney (Audio)
Offers high-quality themed packs that cover the basic needs of almost any prototype or commercial game.
* **License:** CC0 (Public Domain).
* **Highlight:** Sets of interface sounds, casino, science fiction, and narrated voices.
* **Link:** [kenney.nl/assets/category:Audio](https://kenney.nl/assets/category:Audio)

### 2. Sonniss (GDC Bundles)
Annually, Sonniss releases massive bundles of high-definition professional audio (Foley) extracted from paid libraries.
* **License:** Royalty-Free (Commercial use permitted).
* **Highlight:** Cinema-quality sounds for environments, weapons, and vehicles.
* **Link:** [sonniss.com/gameaudiogdc](https://sonniss.com/gameaudiogdc/)

### 3. Freesound.org
A huge collaborative platform where users from all over the world share field recordings and experimental sound effects.
* **Highlight:** Very efficient tag-based search system for specific and organic sounds.
* **Link:** [freesound.org](https://freesound.org/)

### 4. Incompetech (Kevin MacLeod)
The most famous site for finding background music for games and videos. It allows filtering by genre, mood, and tempo.
* **License:** Generally CC-BY (Requires attribution).
* **Highlight:** Varied instrumental tracks that fit into many different contexts.
* **Link:** [incompetech.com/music/](https://incompetech.com/music/royalty-free/music.html)

---

## License Comparison Table (Audio)

| Site | Standard License | Credits Required? | Commercial Use? |
| :--- | :--- | :--- | :--- |
| **Kenney** | CC0 | No | Yes |
| **Soniss** | Royalty-Free | No | Yes |
| **Freesound** | Varies (CC0, CC-BY) | Depends on license | Yes |
| **Incompetech** | CC-BY | Yes | Yes |