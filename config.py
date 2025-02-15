import os
from time import perf_counter
from saveload import SaveLoad
from constants import PARAM_SEP, EXIT_ERR, EXIT_ERR_STR, EXIT_SUCCESS, CONFIG_FILE, PATH_NOT_FOUND
from constants import COLLECTION_SEP, ERROR_LST


class Config:

    IMAGE_EXTENSIONS: tuple[str, ...] = 'png', 'bmp'
    AVAILABLE_ENCODING: tuple[str, ...] = 'utf-8', 'utf-16', 'utf-32', 'cp866', 'cp1251', 'latin-1'
    PARAM_NAMES: tuple[str, ...] = (
        'WND_SCALE',
        'WND_OPACITY',
        'WND_TITLE',
        'WND_ICON_PATH',
        'FONT_PATH',
        'OUTPUT_ENCODING',
        'TB_BACKGROUND_COLOR',
        'TB_BUTTONS_COLOR',
        'TB_FONT_COLOR',
        'INPB_BACKGROUND_COLOR',
        'INPB_FONT_COLOR',
        'TERMINAL_BG_COLOR',
        'TERMINAL_FONT_COLOR',
        'TERMINAL_PROMPT_SYMBOL',
        'TERMINAL_BG_IMAGE',
        'TERMINAL_IMAGE_SCALE',
        'CREATE_NEW_TERMINAL_WORD',
        'DELETE_TERMINAL_WORD',
        'SWITCH_TO_TERMINAL_WORD',
        'PREV_COMMAND_WORD',
        'CLEAR_CMD_STORY_WORD',
        'QUIT_WORD'
    )
    WND_SCALE: float = 0
    WND_OPACITY: float = 0
    TERMINAL_IMAGE_SCALE: float = 0
    WND_TITLE: str = ''
    WND_ICON_PATH: str = ''
    FONT_PATH: str = ''
    OUTPUT_ENCODING: str = ''
    TERMINAL_PROMPT_SYMBOL: str = ''
    TERMINAL_BG_IMAGE: str = ''
    TERMINAL_IMAGE: str = ''
    CREATE_NEW_TERMINAL_WORD: str = ''
    DELETE_TERMINAL_WORD: str = ''
    SWITCH_TO_TERMINAL_WORD: str = ''
    PREV_COMMAND_WORD: str = ''
    QUIT_WORD: str = ''
    CLEAR_CMD_STORY_WORD: str = ''
    TB_BACKGROUND_COLOR: list[int] = []
    TB_BUTTONS_COLOR: list[int] = []
    TB_FONT_COLOR: list[int] = []
    INPB_BACKGROUND_COLOR: list[int] = []
    INPB_FONT_COLOR: list[int] = []
    TERMINAL_BG_COLOR: list[int] = []
    TERMINAL_FONT_COLOR: list[int] = []
    SIZE: int = 64

    @staticmethod
    def init_config() -> int:
        start: float = perf_counter()
        data: str = Config.get_config()
        if data == EXIT_ERR_STR:
            return EXIT_ERR
        data_lst: list[str] = data.replace(' ', '').split('\n')
        i: int = 0
        for pair in data_lst:
            if PARAM_SEP in pair:
                name, value = pair.split(PARAM_SEP)
            else:
                continue
            try:
                if name == 'WND_SCALE':
                    Config.WND_SCALE = float(value.replace(',', '.'))
                    check_scale: int = Config.check_value_bounds(
                        'WND_SCALE',
                        Config.WND_SCALE,
                        0,
                        1)
                    if check_scale == EXIT_ERR:
                        print('Exit the program because of incorrect value of WND_SCALE!', end='\n')
                        break
                    size: int = int(Config.WND_SCALE * Config.SIZE)
                    Config.SIZE = size
                    i += 1
                elif name == 'TERMINAL_IMAGE_SCALE':
                    if value == '':
                        print('Empty value of TERMINAL_IMAGE_SCALE!', end='\n')
                        print('Continue with value=1!', end='\n')
                        Config.TERMINAL_IMAGE_SCALE = 1
                    else:
                        Config.TERMINAL_IMAGE_SCALE = float(value.replace(',', '.'))
                    i += 1
                elif name == 'WND_OPACITY':
                    Config.WND_OPACITY = float(value.replace(',', '.'))
                    check_opacity: int = Config.check_value_bounds(
                        'WND_OPACITY',
                        Config.WND_OPACITY,
                        0,
                        1)
                    if check_opacity == EXIT_ERR:
                        print('Exit the program because of incorrect value of WND_OPACITY!', end='\n')
                        break
                    i += 1
                elif name == 'WND_TITLE':
                    Config.WND_TITLE = value if (value != '') else 'CoffeeTortoiseTerminal'
                    i += 1
                elif name == 'CLEAR_CMD_STORY_WORD':
                    Config.CLEAR_CMD_STORY_WORD = value if (value != '') else 'clear story'
                    i += 1
                elif name == 'PREV_COMMAND_WORD':
                    Config.PREV_COMMAND_WORD = value if (value != '') else 'prev'
                    i += 1
                elif name == 'QUIT_WORD':
                    Config.QUIT_WORD = value if (value != '') else 'close'
                    i += 1
                elif name == 'CREATE_NEW_TERMINAL_WORD':
                    Config.CREATE_NEW_TERMINAL_WORD = value if (value != '') else 'create new'
                    i += 1
                elif name == 'DELETE_TERMINAL_WORD':
                    Config.DELETE_TERMINAL_WORD = value if (value != '') else 'delete terminal'
                    i += 1
                elif name == 'SWITCH_TO_TERMINAL_WORD':
                    Config.SWITCH_TO_TERMINAL_WORD = value if (value != '') else 'switch'
                    i += 1
                elif name == 'TERMINAL_PROMPT_SYMBOL':
                    Config.TERMINAL_PROMPT_SYMBOL = value if (value != '') else '🐧'
                    i += 1
                elif name == 'OUTPUT_ENCODING':
                    if any([value == encod for encod in Config.AVAILABLE_ENCODING]):
                        Config.OUTPUT_ENCODING = value
                        i += 1
                    else:
                        print(f'Encoding {value} is not available!', end='\n')
                        print('Available encodings:\n')
                        [print(f'{i}) {encoding}', end='\n') for i, encoding in enumerate(Config.AVAILABLE_ENCODING, start=1)]
                        print('Exit the program because of incorrect value of OUTPUT_ENCODING!', end='\n')
                        break
                elif name == 'WND_ICON_PATH':
                    img_path: str = value.replace('\'', '').replace('\"', '')
                    icon_path: str = img_path.replace('\\', '/')
                    print('Main window icon image check', end='\n')
                    is_img: int = Config.check_image(icon_path)
                    Config.WND_ICON_PATH = PATH_NOT_FOUND if (is_img == EXIT_ERR) else icon_path
                    i += 1
                elif name == 'TERMINAL_BG_IMAGE':
                    img_path: str = value.replace('\'', '').replace('\"', '')
                    bg_path: str = img_path.replace('\\', '/')
                    print('Terminal background image check', end='\n')
                    is_img: int = Config.check_image(bg_path)
                    Config.TERMINAL_BG_IMAGE = PATH_NOT_FOUND if (is_img == EXIT_ERR) else bg_path
                    i += 1
                elif name == 'FONT_PATH':
                    fnt_path: str = value.replace('\'', '').replace('\"', '')
                    font_path: str = fnt_path.replace('\\', '/')
                    print('Check font path', end='\n')
                    check_fnt: int = Config.check_font(font_path)
                    if check_fnt == EXIT_ERR:
                        print('Exit the program because of incorrect value of FONT_PATH')
                        break
                    else:
                        Config.FONT_PATH = font_path
                        i += 1
                elif name == 'TB_BACKGROUND_COLOR':
                    Config.TB_BACKGROUND_COLOR = Config.lst_from_str(value, is_int=True, is_float=False)
                    if Config.TB_BACKGROUND_COLOR == ERROR_LST:
                        print('Exit the program because of incorrect value of TB_BACKGROUND_COLOR!', end='\n')
                        break
                    check_clr: int = Config.check_collection(
                        'TB_BACKGROUND_COLOR',
                        Config.TB_BACKGROUND_COLOR,
                        3,
                        0,
                        255
                    )
                    if check_clr == EXIT_ERR:
                        print('Exit the program because of incorrect value!', end='\n')
                        break
                    else:
                        i += 1
                elif name == 'TB_BUTTONS_COLOR':
                    Config.TB_BUTTONS_COLOR = Config.lst_from_str(value, is_int=True, is_float=False)
                    if Config.TB_BUTTONS_COLOR == ERROR_LST:
                        print('Exit the program because of incorrect value of TB_BUTTONS_COLOR!', end='\n')
                        break
                    check_clr: int = Config.check_collection(
                        'TB_BUTTONS_COLOR',
                        Config.TB_BUTTONS_COLOR,
                        3,
                        0,
                        255
                    )
                    if check_clr == EXIT_ERR:
                        print('Exit the program because of incorrect value of TB_BUTTONS_COLOR!', end='\n')
                        break
                    else:
                        i += 1
                elif name == 'TB_FONT_COLOR':
                    Config.TB_FONT_COLOR = Config.lst_from_str(value, is_int=True, is_float=False)
                    if Config.TB_FONT_COLOR == ERROR_LST:
                        print('Exit the program because of incorrect value of TB_FONT_COLOR!', end='\n')
                        break
                    check_clr: int = Config.check_collection(
                        'TB_FONT_COLOR',
                        Config.TB_FONT_COLOR,
                        3,
                        0,
                        255
                    )
                    if check_clr == EXIT_ERR:
                        print('Exit the program because of incorrect value of TB_FONT_COLOR!', end='\n')
                        break
                    else:
                        i += 1
                elif name == 'INPB_BACKGROUND_COLOR':
                    Config.INPB_BACKGROUND_COLOR = Config.lst_from_str(value, is_int=True, is_float=False)
                    if Config.INPB_BACKGROUND_COLOR == ERROR_LST:
                        print('Exit the program because of incorrect value of INPB_BACKGROUND_COLOR!', end='\n')
                        break
                    check_clr: int = Config.check_collection(
                        'INPB_BACKGROUND_COLOR',
                        Config.INPB_BACKGROUND_COLOR,
                        3,
                        0,
                        255
                    )
                    if check_clr == EXIT_ERR:
                        print('Exit the program because of incorrect value of INPB_BACKGROUND_COLOR', end='\n')
                        break
                    else:
                        i += 1
                elif name == 'INPB_FONT_COLOR':
                    Config.INPB_FONT_COLOR = Config.lst_from_str(value, is_int=True, is_float=False)
                    if Config.INPB_FONT_COLOR == ERROR_LST:
                        print('Exit the program because of incorrect value of INPB_FONT_COLOR!', end='\n')
                        break
                    check_clr: int = Config.check_collection(
                        'INPB_FONT_COLOR',
                        Config.INPB_FONT_COLOR,
                        3,
                        0,
                        255
                    )
                    if check_clr == EXIT_ERR:
                        print('Exit the program because of incorrect value of INPB_FONT_COLOR!', end='\n')
                        break
                    else:
                        i += 1
                elif name == 'TERMINAL_BG_COLOR':
                    Config.TERMINAL_BG_COLOR = Config.lst_from_str(value, is_int=True, is_float=False)
                    if Config.TERMINAL_BG_COLOR == ERROR_LST:
                        print('Exit the program because of incorrect value of TERMINAL_BG_COLOR!', end='\n')
                        break
                    check_clr: int = Config.check_collection(
                        'TERMINAL_BG_COLOR',
                        Config.TERMINAL_BG_COLOR,
                        3,
                        0,
                        255
                    )
                    if check_clr == EXIT_ERR:
                        print('Exit the program because of incorrect value of TERMINAL_BG_COLOR!', end='\n')
                        break
                    else:
                        i += 1
                elif name == 'TERMINAL_FONT_COLOR':
                    Config.TERMINAL_FONT_COLOR = Config.lst_from_str(value, is_int=True, is_float=False)
                    if Config.TERMINAL_FONT_COLOR == ERROR_LST:
                        print('Exit the program because of incorrect value of TERMINAL_FONT_COLOR!', end='\n')
                        break
                    check_clr: int = Config.check_collection(
                        'TERMINAL_FONT_COLOR',
                        Config.TERMINAL_FONT_COLOR,
                        3,
                        0,
                        255
                    )
                    if check_clr == EXIT_ERR:
                        print('Exit the program because of incorrect value of TERMINAL_FONT_COLOR!', end='\n')
                        break
                    else:
                        i += 1
            except ValueError as e:
                print(f'Error while setting {name} to {value}!\n{e}', end='\n')
        if i != len(Config.PARAM_NAMES):
            print('Quantitative parameter mismatch when reading configuration file!', end='\n')
            print(f'Found {i} instead of {len(Config.PARAM_NAMES)} parameters!', end='\n')
            print('Required parameters:\n')
            [print(f'{i}) {param}') for i, param in enumerate(Config.PARAM_NAMES, start=1)]
            return EXIT_ERR
        else:
            end: float = perf_counter()
            delta: float = end - start
            print(f'The configuration was received in {delta} seconds!', end='\n')
            return EXIT_SUCCESS


    @staticmethod
    def get_config() -> str:
        config: str = Config.find_config_file()
        if config == EXIT_ERR_STR:
            return EXIT_ERR_STR
        data: str = SaveLoad.load(config)
        if data == EXIT_ERR_STR:
            return EXIT_ERR_STR
        return data

    @staticmethod
    def find_config_file() -> str:
        try:
            cwd: str = os.getcwd()
            files: list[str] = [f for f in os.listdir(cwd) if os.path.isfile(f)]
            for file in files:
                if CONFIG_FILE in file:
                    return file
            for root, dirs, files in os.walk('/'):
                for item in dirs + files:
                    full_path: str = os.path.join(root, item)
                    if CONFIG_FILE in full_path:
                        print(f'Configuration file found at {full_path}!', end='\n')
                        return full_path
            print(f'Couldn\'t find {CONFIG_FILE}!', end='\n')
            return EXIT_ERR_STR
        except OSError as e:
            print(f'While searching {CONFIG_FILE}, something went wrong!\n{e}', end='\n')
            return EXIT_ERR_STR

    @staticmethod
    def check_image(path: str) -> int:
        check_filepath: int = SaveLoad.check_filepath(path)
        if check_filepath == EXIT_ERR:
            return EXIT_ERR
        if not any([path.endswith(ext) for ext in Config.IMAGE_EXTENSIONS]):
            print(f'{path} has incorrect extension!', end='\n')
            print('Available image extensions:', end='\n')
            [print(f'{i}) {ext}') for i, ext in enumerate(Config.IMAGE_EXTENSIONS, start=1)]
            return EXIT_ERR
        print('Correct image!', end='\n')
        return EXIT_SUCCESS

    @staticmethod
    def check_font(path: str) -> int:
        check_filepath: int = SaveLoad.check_filepath(path)
        if check_filepath == EXIT_ERR:
            return EXIT_ERR
        if not path.endswith('ttf'):
            print(f'{path} has incorrect extension!', end='\n')
            print('The font file extension must be ttf!', end='\n')
            return EXIT_ERR
        print('Correct font!', end='\n')
        return EXIT_SUCCESS

    @staticmethod
    def check_value_bounds(
            value_name: str,
            value: int | float,
            begin: int | float,
            end: int | float
    ) -> int:
        if (value < begin) or (value > end):
            print(f'The value of {value_name} must be between {begin} and {end} inclusive!\n')
            return EXIT_ERR
        return EXIT_SUCCESS

    @staticmethod
    def check_collection(
            value_name: str,
            collection: list | tuple,
            length: int,
            begin: int | float,
            end: int | float
    ) -> int:
        if len(collection) != length:
            print(f'{value_name} must have length {length}, not {len(collection)}!', end='\n')
            return EXIT_ERR
        for i, value in enumerate(collection, start=1):
            name: str = f'Variable {i} of collection {value_name}'
            check_val: int = Config.check_value_bounds(
                name,
                value,
                begin,
                end
            )
            if check_val == EXIT_ERR:
                print('Incorrect value!')
                return EXIT_ERR
        return EXIT_SUCCESS

    @staticmethod
    def lst_from_str(value: str,
                     is_int: bool = True,
                     is_float: bool = False) -> list[int | float | str]:
        src: list[str] = value.replace(' ', '').split(COLLECTION_SEP)
        if len(src) < 1:
            print('Length of src must not be less then 1!', end='\n')
            print(f'All values must be separated with {COLLECTION_SEP}', end='\n')
            return ERROR_LST
        try:
            if is_int:
                res: list[int] = list(map(lambda i: int(i), src))
            elif is_float:
                res: list[float] = list(map(lambda i: float(i.replace(',', '.')), src))
            else:
                return src
            return res
        except ValueError as e:
            print(f'Cannot create list of numbers from {value}!\n{e}', end='\n')
            return ERROR_LST
