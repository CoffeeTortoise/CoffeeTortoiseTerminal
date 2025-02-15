from PyQt6.QtWidgets import QWidget, QMainWindow, QTextEdit, QLabel
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from typing import Any
import os
import sys
from config import Config
from toolbar import Toolbar
from terminal import Terminal
from constants import EXIT_STR, EXIT_SUCCESS
from inputer import run_command


class InputText(QTextEdit):

    def __init__(self,
                 parent: QWidget | QMainWindow,
                 term_parent: QWidget | QMainWindow,
                 linked_toolbar: Toolbar,
                 term_size: tuple[int, int],
                 term_pos: tuple[int, int]) -> None:
        super().__init__(parent)
        self.toolbar: Toolbar = linked_toolbar
        self.enter_pressed: bool = False
        self.current_text: str = ''
        self.cmd_story: list[str] = []
        self.terminals: list[Terminal] = [Terminal(term_parent, term_size, term_pos)]
        self.active_terminal: Terminal = self.terminals[0]
        self.term_params: list[Any] = [term_parent, term_size, term_pos]
        self.active_terminal.show()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if isinstance(event, QKeyEvent):
            if (event.key() == Qt.Key.Key_Return) and not self.enter_pressed:
                self.enter_pressed = True
            elif (event.key() == Qt.Key.Key_Shift) and self.enter_pressed:
                self.current_text = self.toPlainText().replace('\n', ' ')
                command_out: tuple[str, ...] = self.execute_prompt()
                self.active_terminal.add_text(f'{command_out[0]}\n{command_out[1]}')
                self.cmd_story.append(self.current_text)
                self.enter_pressed = False
            else:
                self.enter_pressed = False
        else:
            self.enter_pressed = False
        super().keyPressEvent(event)

    def execute_prompt(self) -> tuple[str, ...]:
        prompt: str = self.current_text
        cwd: str = os.getcwd()
        com_try: str = f'{cwd}{Config.TERMINAL_PROMPT_SYMBOL}>\n' + prompt + '\n'
        self.active_terminal.add_text(com_try)
        if prompt.replace(' ', '') == Config.CREATE_NEW_TERMINAL_WORD.replace(' ', ''):
            self.toolbar.add_term_lbl()
            self.terminals.append(Terminal(*self.term_params))
            self.setText('')
            return prompt, EXIT_STR
        elif prompt.replace(' ', '') == Config.CLEAR_CMD_STORY_WORD.replace(' ', ''):
            self.cmd_story.clear()
            self.setText('')
            return prompt, EXIT_STR
        elif Config.DELETE_TERMINAL_WORD.replace(' ', '') in prompt.replace(' ', ''):
            self.setText('')
            try:
                n: str = prompt[len(Config.DELETE_TERMINAL_WORD) + 1:].replace(' ', '')
                num: int = int(n)
                if num == 0:
                    return prompt, 'Cannot delete base terminal'
                elif num > self.toolbar.term_cntr:
                    return prompt, f'Terminal with index {num} doesn\'t exist'
                else:
                    self.active_terminal = self.terminals[0]
                    del self.terminals[num]
                    self.toolbar.layer.itemAt(num - 1).widget().setParent(None)
                    self.toolbar.term_cntr -= 1
                    j: int = 1
                    for i in range(self.toolbar.layer.count()):
                        widget: QLabel | Any = self.toolbar.layer.itemAt(i).widget()
                        if type(widget) is QLabel:
                            widget.setText(str(j))
                            j += 1
                    return prompt, f'{EXIT_STR}\nActive terminal is base terminal'
            except ValueError as e:
                return prompt, f'{e}'
            except IndexError as e:
                return prompt, f'{e}'
        elif Config.SWITCH_TO_TERMINAL_WORD.replace(' ', '') in prompt.replace(' ', ''):
            n: str = prompt[len(Config.SWITCH_TO_TERMINAL_WORD) + 1:].replace(' ', '')
            self.setText('')
            try:
                num: int = int(n)
                if num < 0:
                    return prompt, 'There are no terminals with a negative index here'
                elif num >= len(self.terminals):
                    return prompt, f'Too big index. There are only {len(self.terminals)} terminals'
                else:
                    self.active_terminal.hide()
                    self.active_terminal = self.terminals[num]
                    self.active_terminal.show()
                    return prompt, f'Terminal with index {num} is now active\n{EXIT_STR}'
            except ValueError as e:
                return prompt, f'{e}'
        elif Config.PREV_COMMAND_WORD.replace(' ', '') in prompt.replace(' ', ''):
            n: str = prompt[len(Config.PREV_COMMAND_WORD) + 1:].replace(' ', '')
            try:
                num: int = int(n)
                if abs(num) >= len(self.cmd_story):
                    self.setText('')
                    return prompt, f'Only {len(self.cmd_story)} have been executed!'
                else:
                    txt: str = self.cmd_story[num]
                    self.setText(txt)
                    return prompt, EXIT_STR
            except ValueError as e:
                self.setText('')
                return prompt, f'{e}'
            except IndexError as e:
                self.setText('')
                return prompt, f'{e}'
        elif Config.QUIT_WORD.replace(' ', '') == prompt.replace(' ', ''):
            self.setText('')
            if Config.TERMINAL_IMAGE != '':
                os.remove(Config.TERMINAL_IMAGE)
            sys.exit(EXIT_SUCCESS)
        else:
            self.setText('')
            command_out: tuple[str, ...] = run_command(prompt)
            return command_out
