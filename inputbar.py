from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.QtGui import QFont
import sys
from inputext import InputText
from constants import EXIT_ERR
from toolbar import Toolbar
from config import Config


class InputBar(QWidget):

    def __init__(self,
                 parent: QWidget | QMainWindow,
                 linked_toolbar: Toolbar,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 term_size: tuple[int, int],
                 term_pos: tuple[int, int]) -> None:
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.move(pos[0], pos[1])

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

        fnt_size: int = int(Config.SIZE * .2)
        self.font: QFont = font
        self.font.setPointSize(fnt_size)
        self.font.setBold(True)

        self.text_wnd: InputText = InputText(self, parent, linked_toolbar, term_size, term_pos)
        self.text_wnd.setFont(self.font)
        self.text_wnd.setFixedSize(size[0], size[1])
        self.text_wnd.move(0, 0)
        txt_wnd_bg: str = '#{:02x}{:02x}{:02x}'.format(*Config.INPB_BACKGROUND_COLOR)
        txt_wnd_fnt: str = '#{:02x}{:02x}{:02x}'.format(*Config.INPB_FONT_COLOR)
        txt_wnd_style: str = f'InputText {{background-color: {txt_wnd_bg}; color: {txt_wnd_fnt}; }}'
        self.text_wnd.setStyleSheet(txt_wnd_style)
        self.text_wnd.show()
