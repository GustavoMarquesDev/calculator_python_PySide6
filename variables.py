from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
FILES_DIR = ROOT_DIR / "files"
WINDOW_ICON_PATH = FILES_DIR / "calculator.ico"


# Sizing
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 18
TEXT_MARGIN = 15
MINIMUM_WIDTH = 500

# Colors
DARK_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'

BACKGROUND_COLOR = '#f5f5f5'  # Cor de fundo padrão
SECONDARY_BACKGROUND_COLOR = '#e0e0e0'  # Cor de fundo secundária
HOVER_COLOR = '#d6d6d6'  # Cor para hover (efeito ao passar o mouse)
BORDER_COLOR = '#cccccc'  # Cor para bordas
PRESSED_COLOR = '#bdbdbd'  # Cor para estados pressionados (ex.: botão clicado)
