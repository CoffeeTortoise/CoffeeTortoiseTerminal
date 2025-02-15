from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from config import Config
from toolbar import Toolbar
from inputbar import InputBar
from constants import EXIT_ERR, PATH_NOT_FOUND
import sys
import os


class CoffeeTerminal(QMainWindow):

    def __init__(self,
                 width: int,
                 height: int,
                 x: int,
                 y: int) -> None:
        super().__init__()
        self.setWindowTitle(Config.WND_TITLE)
        self.setFixedSize(width, height)
        self.setWindowOpacity(Config.WND_OPACITY)
        self.move(x, y)
        try:
            if Config.WND_ICON_PATH != PATH_NOT_FOUND:
                icon: QIcon = QIcon(Config.WND_ICON_PATH)
                self.setWindowIcon(icon)
        except PermissionError as e:
            print(f'Not enough rights to use {Config.WND_ICON_PATH} as icon!\n{e}', end='\n')
        except ValueError as e:
            print(f'The format of icon {Config.WND_ICON_PATH} is not supported!\n{e}', end='\n')
        except OSError as e:
            print(f'Something went wrong when setting {Config.WND_ICON_PATH}!\n{e}', end='\n')
        except Exception as e:
            print(f'Something went wrong when setting {Config.WND_ICON_PATH}!\n{e}', end='\n')

        size: tuple[int, int] = Config.SIZE * 26, int(Config.SIZE * 1.3)
        pos: tuple[int, int] = 0, 0
        self.tb: Toolbar = Toolbar(self, size, pos)
        self.tb.show()

        inb_size: tuple[int, int] = Config.SIZE * 26, Config.SIZE * 2
        inb_pos: tuple[int, int] = 0, height - inb_size[1]
        t_height: int = inb_pos[1] - size[1]
        term_size: tuple[int, int] = inb_size[0], t_height
        term_pos: tuple[int, int] = 0, size[1]
        self.inp_bar: InputBar = InputBar(self, self.tb, inb_size, inb_pos, term_size, term_pos)
        self.inp_bar.show()


def main() -> int:
    is_inited: int = Config.init_config()
    if is_inited == EXIT_ERR:
        print('Error when receiving configuration parameters!', end='\n')
        return EXIT_ERR
    app: QApplication = QApplication(sys.argv)
    width: int = Config.SIZE * 26
    height: int = Config.SIZE * 15
    x: int = 100
    y: int = 50
    coffee_terminal: CoffeeTerminal = CoffeeTerminal(
        int(width),
        int(height),
        int(x),
        int(y))
    coffee_terminal.show()
    return app.exec()


if __name__ == '__main__':
    print('The application: CoffeeTortoiseTerminal starts running!', end='\n')
    running: bool = True
    status: int = 0
    while running:
        status = main()
        res: str = input('Enter q or quit to close the program: ').lower()
        if (res == 'q') or (res == 'quit'):
            running = False
    if Config.TERMINAL_IMAGE != '':
        os.remove(Config.TERMINAL_IMAGE)
    print('CoffeeTortoiseTerminal closed!', end='\n')
    sys.exit(status)