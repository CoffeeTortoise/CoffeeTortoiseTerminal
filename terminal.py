from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
import sys
from constants import EXIT_ERR, EXIT_SUCCESS, PATH_NOT_FOUND
from imgworker import image_worker
from config import Config


class Terminal(QWidget):

    DY: int = 0
    FONT: QFont = QFont()
    FNT_SIZE: int = 1
    HAS_FNT: bool = False

    def __init__(self,
                 parent: QMainWindow | QWidget,
                 size: tuple[int, int],
                 pos: tuple[int, int]) -> None:
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.move(pos[0], pos[1])

        r, g, b = Config.TERMINAL_BG_COLOR
        self.widget: QWidget = QWidget(self)
        self.widget.setFixedSize(size[0], size[1])
        self.widget.move(0, 0)
        bg_clr: str = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        fnt_clr: str = '#{:02x}{:02x}{:02x}'.format(*Config.TERMINAL_FONT_COLOR)

        Terminal.init_font()

        self.layer: QVBoxLayout = QVBoxLayout(self.widget)
        self.layer.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroller: QScrollArea = QScrollArea(self)
        self.scroller.setFixedSize(size[0], size[1])
        self.scroller.move(0, 0)

        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.widget)

        self.bg_img_status: int = EXIT_SUCCESS
        if Config.TERMINAL_BG_IMAGE != PATH_NOT_FOUND:
            try:
                if Config.TERMINAL_IMAGE == '':
                    _, h = image_worker(Config.TERMINAL_BG_IMAGE, Config.TERMINAL_IMAGE_SCALE)
                    Terminal.DY = h + Config.SIZE
                bg_img: str = f'background-image: url({Config.TERMINAL_IMAGE});'
                bg_attach: str = 'background-attachment: fixed;'
                bg_repeat: str = 'background-repeat: repeat-y;'
                bg_pos: str = 'background-position: center;'
                bg_style: str = bg_img + bg_attach + bg_repeat + bg_pos
                self.bg_sheet: str = f'QWidget {{{bg_style}}}'
                self.widget.setStyleSheet(self.bg_sheet)
            except PermissionError as e:
                print(f'Not enough rights to use {Config.TERMINAL_BG_IMAGE}!\n{e}', end='\n')
                self.bg_img_status: int = EXIT_ERR
            except ValueError as e:
                print(f'The format of {Config.TERMINAL_BG_IMAGE} is not supported!\n{e}', end='\n')
                self.bg_img_status: int = EXIT_ERR
            except OSError as e:
                print(f'Something went wrong when loading {Config.TERMINAL_BG_IMAGE}\n{e}', end='\n')
                self.bg_img_status: int = EXIT_ERR
            except Exception as e:
                print(f'Something went wrong when loading {Config.TERMINAL_BG_IMAGE}\n{e}', end='\n')
                self.bg_img_status: int = EXIT_ERR
        else:
            self.bg_img_status: int = EXIT_ERR
        if self.bg_img_status == EXIT_ERR:
            self.set_widget_palette()
            self.txt_style: str = f'QLabel {{background-color: {bg_clr}; color: {fnt_clr};}}'
            self.bg_sheet: str = ''
            h: int = self.widget.height()
            if Terminal.DY == 0:
                Terminal.DY = h
        else:
            self.txt_style: str = f'QLabel {{background-color: rgba(0, 0, 0, 0); color: {fnt_clr};}}'

    def add_text(self,
                 text: str) -> None:
        lines: int = text.count('\n')
        width: int = self.width()
        height: int = int(Terminal.FNT_SIZE * lines * 3)
        w_width, w_height = self.widget.width(), self.widget.height()
        if height > Terminal.DY:
            w_height += height
            size: tuple[int, int] = width, height
        else:
            w_height += Terminal.DY
            size: tuple[int, int] = width, Terminal.DY
        txt: QLabel = QLabel(text, self.widget)
        txt.setFixedSize(size[0], size[1])
        txt.setFont(Terminal.FONT)
        txt.setStyleSheet(self.txt_style)
        self.layer.addWidget(txt)
        self.widget.setFixedSize(w_width, w_height)

    def set_widget_palette(self) -> None:
        palette: QPalette = self.widget.palette()
        palette.setColor(self.widget.backgroundRole(), QColor(*Config.TERMINAL_BG_COLOR))
        self.widget.setPalette(palette)
        self.widget.setAutoFillBackground(True)

    @staticmethod
    def init_font() -> None:
        if Terminal.HAS_FNT:
            return

        try:
            Terminal.FONT.setFamily(Config.FONT_PATH)
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

        Terminal.FNT_SIZE = int(Config.SIZE * .2)
        Terminal.FONT.setPointSize(Terminal.FNT_SIZE)
        Terminal.FONT.setBold(True)
        Terminal.HAS_FNT = True
