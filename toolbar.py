from PyQt6.QtWidgets import QWidget, QMainWindow, QHBoxLayout, QLabel
from PyQt6.QtGui import QPalette, QColor, QFont
import sys
from constants import EXIT_ERR
from config import Config


class Toolbar(QWidget):

    def __init__(self,
                 parent: QMainWindow | QWidget,
                 size: tuple[int, int],
                 pos: tuple[int, int]) -> None:
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.move(pos[0], pos[1])
        palette: QPalette = self.palette()
        r, g, b = Config.TB_BACKGROUND_COLOR
        palette.setColor(self.backgroundRole(), QColor(r, g, b))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.layer: QHBoxLayout = QHBoxLayout(self)

        try:
            font: QFont = QFont(Config.FONT_PATH)
        except PermissionError as e:
            print(f'Not enough rights to use {Config.FONT_PATH} as font!\n{e}', end='\n')
            sys.exit(EXIT_ERR)
        except ValueError as e:
            print(f'Font format of {Config.FONT_PATH} is not supported!\n{e}', end='\n')
            sys.exit(EXIT_ERR)
        except OSError as e:
            print(f'Failed to create font from {Config.FONT_PATH}\n{e}', end='\n')
            sys.exit(EXIT_ERR)
        except Exception as e:
            print(f'Failed to create font from {Config.FONT_PATH}\n{e}', end='\n')
            sys.exit(EXIT_ERR)

        fnt_size: int = int(Config.SIZE * .3)
        self.font: QFont = font
        self.font.setPointSize(fnt_size)
        self.font.setBold(True)

        bg_clr: str = '#{:02x}{:02x}{:02x}'.format(*Config.TB_BUTTONS_COLOR)
        txt_clr: str = '#{:02x}{:02x}{:02x}'.format(*Config.TB_FONT_COLOR)
        self.lbl_style: str = f'QLabel {{background-color: {bg_clr}; color: {txt_clr}}}'
        self.term_cntr: int = 0
        self.lbl_size: tuple[int, int] = int(Config.SIZE * .7), int(Config.SIZE * .7)

    def add_term_lbl(self) -> None:
        self.term_cntr += 1
        lbl: QLabel = QLabel(str(self.term_cntr), self)
        lbl.setFont(self.font)
        lbl.setFixedSize(self.lbl_size[0], self.lbl_size[1])
        lbl.setStyleSheet(self.lbl_style)
        lbl.show()
        self.layer.addWidget(lbl)
