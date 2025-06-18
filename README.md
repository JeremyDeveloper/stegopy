# stegopy 🦖

> A deterministic, no-magic Python toolkit for hiding messages in media.
>   
> Built during a hyperfixation spiral that got wildly out of hand — and I'm not even sorry.
> 
> Clean enough for clarity. Fast enough for scale.


```
              __
             / _)
     _.----._/ /
   /         /
__|  (|_|_|_|
  `--' `-'-'  
  
  Because if you’re hiding data like a stealth dino,
you deserve a dino.
```
*I haven’t slept in 72 hours and I know where every bit is.*

## 📦 What is this?

**stegopy** is a zero-bloat, bit-accurate steganography library for embedding UTF-8 messages in images and audio.  It was built with obsessive attention to structure, correctness, and minimalism.

No unnecessary abstractions. No guesswork.  
Every bit has a reason to be where it is.

## 🎯 Core Philosophy

This library exists because I wanted:

- Full visibility into **how** messages are embedded
- File formats I could **actually understand**
- Bit-aligned logic I didn’t have to reverse-engineer from StackOverflow
- A reason to stop thinking about it at 3AM
  
It is not built for configurability. It’s built for **peace of mind** — the kind that comes from predictable behavior and clean code.

## ✅ Features

- 🖼️ Image Steganography
  - Hide text or images inside other images
  - RGB LSB embedding (actually easy to reason about)
  - R/G/B channel-only mode, if you're picky
  - Alpha channel encoding — the closest you’ll get to invisible
  - Region targeting (center, corners, you name it)
  - Fully combinable: region + channel + alpha? Yes.

- 🔊 Audio Steganography
  - Hide text or images inside **16-bit PCM mono WAV and AIFF** files
  - Bit-level LSB encoding across all samples
  - Same predictable, reversible structure as image hiding

- 🔤 Full UTF-8 compatibility (multi-byte safe, emoji-friendly)
- 🧪 **40+ unit tests** — full coverage with low execution time
- 📚 Every function includes docstrings, error handling, and input checks
- 🧱 No dependencies (except Pillow)
- ⚡ Fast enough for high-volume batch stego with zero overhead
- 🦖 CLI with ASCII dinosaurs? You better believe it.

⚠️ **Not for people who ask “but why doesn’t it do JPEG?”**
## 🧠 Why Use stegopy?

Because sometimes, you want to know *exactly* what’s happening under the hood.  
This library is built for minds that crave:

- 📐 Precision
- 💡 Predictability
- 🧩 Byte-level understanding

It's not “magical.”  
It’s **deliberate**.

It’s not “easy.”  
It’s **exact**.

## 🔍 Install

```bash
pip install stegopy
```

(or install from source if you're a dev:)
```bash
git clone https://github.com/viodoescyber/stegopy
cd stegopy
pip install .
```

## 🔐 Usage Examples

### 🖼️ Encode in an Image

```py
from stegopy.image import lsb

lsb.encode("cat.png", "cat_out.png", "hyperfixation? what hyperfixation?")
print(lsb.decode("cat_out.png"))
```

Use a specific color channel:
```py
from stegopy.image import color
color.encode("input.png", "out.png", "Green is mathematically optimal.", channel="g")
```

Maybe hide in the alpha channel?
```py
from stegopy.image import alpha
alpha.encode("alpha.png", "out.png", "This is invisible but the data is STILL PERFECTLY STRUCTURED")
```

Use only the center pixels (or corners!):
```py
from stegopy.image import region
region.encode("map.png", "out.png", "Just top left. That's all I need.", region="topleft")
```

Or combine it all:
```py
from stegopy.image import combo
combo.encode("canvas.png", "output.png", "Combo activated 💥", channel="b", region="center")
```
Yes, this works with any mix: region + alpha, channel + region, just alpha, or none at all. It Just Works™.

### 🔊 Encode in Audio

```py
from stegopy.audio import lsb

lsb.encode("input.wav", "stego.wav", "I encoded this while pacing around my room for 2 hours straight")
print(lsb.decode("stego.wav"))
```
⚠️ Only accepts 16-bit mono PCM WAV and AIFF files — this is intentional.

## 🧰 Command-Line Interface (CLI)

Once installed, just run:
```bash
stegopy [message] <-e/--encode | -d/--decode> <-i input> [-o output] [--channel r/g/b] [--alpha]
```

### 🔧 CLI Usage Examples

Capacity estimation:
```bash
stegopy -i input.png -c
# 🧠 Estimated capacity: 1024 UTF-8 characters
```

Encode a message into an image:
```bash
stegopy "i belong in the LSB" -e -i cat.png -o secret.png
```

Decode from the same image:
```bash
stegopy -d -i output.png
```

Hide it in a specific channel:
```bash
stegopy "color-coded secrets" -e -i input.png -o out.png --channel g
```

Encode in the alpha layer:
```bash
stegopy "ghost text" -e -i transparent.png -o result.png --alpha
```

Combine with region targeting:
```bash
stegopy "top left green channel go brr" -e -i input.png -o out.png --channel g --region topleft
```

Embed an image into another image:
```bash
stegopy payload.png -e -i carrier.png -o out.png
```

Decode and auto-save if its an image:
```bash
stegopy -d -i out.png -o carrier.png
```

For audio:
```bash
stegopy "auditory hyperfixation" -e -i input.wav -o result.wav
stegopy -d -i result.wav
```
```bash
stegopy payload.png -e -i carrier.wav -o out.wav
stegopy -d -i out.wav -o carrier.png
```
❗ Only 16-bit PCM mono WAVs and AIFFs allowed. If you're here trying to LSB a `.flac`, I’m going to assume you're from the future.