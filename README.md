# CoffeeTortoiseTerminal

Pretty customizable terminal on pyqt6.

## Configuration file

Name of the configuration file COFFEE_TORTOISE_TERMINAL_CONFIG.txt

Parameters: 
1. WND_SCALE: Defines the window size. It can be in the range from 0 to 1.
2. WND_OPACITY: Defines the window opacity. It can be in the range from 0 to 1.
3. WND_TITLE: Window title. That's obvious. Optional value.
4. WND_ICON_PATH: Path to window icon.Accepts png and bmp images.
5. TB_BACKGROUND_COLOR: The color of area at the top where the indexes of the currently existing windows will be displayed. Indexing starts from 0. Accepts 3 integer non-negative variables, each of which can take a value from 0 to 255. Variables must be separated by the character ','. The same is true for other colors.
6. TB_BUTTONS_COLOR: The color of the placemark with the window index.
7. TB_FONT_COLOR: Label font color
8. TERMINAL_BG_COLOR: The background color of the terminal. It is ignored if the terminal window has an image as a background.
9. TERMINAL_FONT_COLOR: The color of the text in the terminal.
10. TERMINAL_PROMPT_SYMBOL: The character followed by the command.
11. TERMINAL_BG_IMAGE: The path to the terminal background image. Optional value.
12. TERMINAL_IMAGE_SCALE: The zoom level of the image for the terminal. Floating point value. Optional value.
13. CREATE_NEW_TERMINAL_WORD: The command to create a new window. Optional value.
14. DELETE_TERMINAL_WORD: The command to delete a window with index. Syntax: DELETE_TERMINAL_WORD window_index. Optional value.
15. SWITCH_TO_TERMINAL_WORD: The command to switch between terminals. Syntax: SWITCH_TO_TERMINAL_WORD window_index. Optional value.
16. CLEAR_CMD_STORY_WORD: Clears the command history for all terminal windows. Optional value.
17. PREV_COMMAND_WORD: The command to get one of previously used command. Syntax: PREV_COMMAND_WORD window_index. Optional value.
18. QUIT_WORD: The command to close terminal. Optional value.
19. INPB_BACKGROUND_COLOR: Background color for the input window.
20. INPB_FONT_COLOR: Font color for the input window.
21. FONT_PATH: The path to the terminal font. Accepts only ttf fonts.
22. OUTPUT_ENCODING: Encoding of the text output. Acceptable encodings: 'utf-8', 'utf-16', 'utf-32', 'cp866', 'cp1251', 'latin-1'.

## Recommendation for use
This terminal was created for educational purposes. It is capable of executing only basic linux console/terminal commands. Also, when using this terminal, you cannot change the current working directory.