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

- Randomized 3x3 slot grid with fruit symbols.
- Dynamic betting with multiple line modes (Horizontal, Diagonal, Both).
- Adjustable bet multiplier (1x to 5x).
- Win evaluation for 3-of-a-kind and 2-of-a-kind payouts.
- Asynchronous game loop for web compatibility using `asyncio`.
- Cross-platform deployment to desktop and web (via `pygbag`).
- Assets are auto-downloaded at runtime.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/baxpicker/vibe-slot.git
    cd vibe-slot
    ```

2.  **(Optional) Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    This will install `pygame` for the game engine and `pygbag` for web deployment.
    ```bash
    pip install pygame pygbag
    ```

## Usage

The game can be run as a native desktop application or as a web application in the browser.

### Web Version (Recommended)

This method compiles the game to WebAssembly and serves it locally, allowing you to play in a web browser.

1.  **Build & Serve:**
    From the project's root directory, run the following command:
    ```bash
    python3 -m pygbag main.py
    ```

2.  **Access in Browser:**
    Once the server starts, open your browser and navigate to:
    [http://localhost:8000](http://localhost:8000)

### Desktop Version

To run the game as a standard desktop application:

```bash
python3 main.py
```

## Controls

-   **Spin**: Press the `SPACE` key.
-   **Change Betting Mode**: Click the `Lines: ...` button.
-   **Change Multiplier**: Click the `Multiplier: ...` button.
-   **Exit**: Close the game window or browser tab.

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
