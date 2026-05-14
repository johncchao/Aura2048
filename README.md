# ✦ Aura2048

> The number dies. The image remains.

A 2048 variant where tiles aren't numbers — they're **visual auras** that evolve as you merge. The higher you climb, the more the numbers fade, until all that's left is pure artwork.

Zero dependencies. One HTML file. Infinite skins.

## Philosophy

Most 2048 clones add complexity. This one removes it.

- Numbers **dissolve** as tiles level up (opacity fades from 0.9 → 0.05)
- At endgame, your board is a gallery, not a spreadsheet
- The merge sound rises in pitch with each evolution — your ears know you're winning before your eyes do

## Features

| | |
|---|---|
| 🎨 Image skins | Any 11 images = a complete theme |
| 🎬 Animations | Slide (easeOutQuad) · Spawn (easeOutBack) · Merge pulse |
| 🔊 Audio | Procedural synth SFX via Web Audio API |
| 📱 Mobile | Touch swipe + Telegram haptic feedback |
| 💾 Persistence | localStorage auto-save/restore |
| 🖼️ Cover-crop | Non-square images handled gracefully |
| ⚡ Performance | Single `<canvas>`, requestAnimationFrame, ~0 GC pressure |

## Quick Start

```bash
open index.html
```

That's it. No build step. No `npm install`. No webpack config longer than your actual code.

## Skin System

Drop 11 images into any folder, change two values:

```js
// In SkinManager config:
skinFolder: 'assets/cyberpunk',   // your folder
skinExt: '.png',                   // your format
```

Files should be named `1.jpg` → `11.jpg` (or `.png`/`.webp`), mapping to tile values 2 → 2048.

Images don't need to be square — the engine center-crops automatically (`object-fit: cover` equivalent).

## Architecture

```
index.html          ← everything (yes, really)
generate_placeholders.py  ← Pillow script for test assets
assets/
  test_skins/       ← placeholder geometric art (1-11.jpg)
```

## Telegram Mini App

Works out of the box as a Telegram Mini App. Includes:
- `telegram-web-app.js` integration
- `HapticFeedback` on merge
- `switchInlineQuery` share on reaching 2048

## License

Do whatever you want. The interesting part isn't the code.
