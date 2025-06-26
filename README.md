# vibe-slot

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/baxpicker/vibe-slot)](LICENSE)

vibe-slot is an AI-powered slot machine game developed in Python using Pygame. Inspired by "vibe coding," it demonstrates automatic code generation to create a fun, interactive fruit-themed slot experience.

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Assets](#assets)
- [Contributing](#contributing)
- [License](#license)

## Demo

Below is a preview of the game in action:

<p align="center">
  <img src="assets/1f352.png" width="64" alt="Cherry"> 
  <img src="assets/1f34b.png" width="64" alt="Lemon"> 
  <img src="assets/1f34a.png" width="64" alt="Orange">
</p>

## Features

- Randomized three-reel slot spin with fruit emojis.
- Win evaluation: 3-of-a-kind or 2-of-a-kind payouts.
- Credit system with spin cost and rewards.
- Smooth spin animation and real-time rendering via Pygame.
- Assets auto-downloaded at runtime from Twitter's Twemoji repository.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/baxpicker/vibe-slot.git
   cd vibe-slot
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install pygame
   ```

## Usage

Run the game with:

```bash
python3 main.py
```

The `assets/` folder will be auto-populated with emoji images on first run.

## Controls

- **SPACE**: Spin the reels.
- **Close Window**: Exit the game.

## Assets

All fruit icons are stored in `assets/` and fetched automatically if missing:

| Symbol | Codepoint | Filename |
| -------| --------- | -------- |
| 🍒     | 1f352     | assets/1f352.png |
| 🍋     | 1f34b     | assets/1f34b.png |
| 🍊     | 1f34a     | assets/1f34a.png |
| 🍉     | 1f349     | assets/1f349.png |
| 🍇     | 1f347     | assets/1f347.png |
| 🍓     | 1f353     | assets/1f353.png |

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to add features, improve graphics, or refine gameplay.

## License

This project is licensed under the [MIT License](LICENSE).
