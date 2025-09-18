# Space Shooter

A simple 2D space shooter built with **Python** and **pygame-ce**.

## Features

* Player movement & shooting
* Falling meteors
* Explosions & sound effects
* Score based on survival time

## Controls

* **Arrow Keys**: Move
* **Space**: Shoot
* **Esc / Close Window**: Quit

## Install & Run

```bash
# Clone the repo
git clone https://github.com/migzster-snow/space-shooter.git
cd space-shooter

# Create venv (optional)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependency
pip install pygame-ce

# Run the game
python main.py
```

## Project Structure

```
space-shooter/
├─ images/        # sprites & font
├─ audio/         # sound effects & music
├─ main.py        # game code
└─ README.md
```

## License

[MIT License](LICENSE)
