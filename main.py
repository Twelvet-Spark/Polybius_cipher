# The Polybius cipher
from enum import Enum, member
import secrets
import random


class Alphabets:
    class Types(Enum):
        cyrillic: list = [chr(index) for index in range(ord("а"), ord("я") + 1)]
        latin: list = [chr(index) for index in range(ord("a"), ord("z") + 1)]

    class Sizes(Enum):
        Latin_Standard = {"x_size": 5, "y_size": 5}
        Cyrillic_Standard = {"x_size": 6, "y_size": 6}
        Cyrillic_SemiMerged = {"x_size": 6, "y_size": 5}
        Cyrillic_FullyMerged = {"x_size": 5, "y_size": 5}

class Methods(Enum):
    @member
    class Method_one:
        """
        Смещение вниз.

        Суть в том, чтобы каждую букву шифруемого слова найти в квадрате Полибия и после брать букву ниже буквы шифруемого слова в квадрате Полибия. Если буква найденная из шифруемого слова является последней в квадрате по вертикали, берут букву первой строки

        Attributes:
            id (int): id метода.
            name (str): Название метода.
            description (str): Описание метода."""
        id: int = 1
        name: str = "Swift down"
        desctiption: str = "Суть в том, чтобы каждую букву шифруемого слова найти в квадрате Полибия и после брать букву ниже буквы шифруемого слова в квадрате Полибия. Если буква найденная из шифруемого слова является последней в квадрате по вертикали, берут букву первой строки"

    @member
    class Method_two:
        """
        Интерполяция координат.

        Сообщение преобразуется в координаты по квадрату Полибия, координаты записываются вертикально, затем координаты считывают по строкам, далее координаты преобразуются в буквы по этому же квадрату

        Attributes:
            id (int): id метода.
            name (str): Название метода.
            description (str): Описание метода."""
        id: int = 2
        name: str = "Coordinates interpolation"
        desctiption: str = "Сообщение преобразуется в координаты по квадрату Полибия, координаты записываются вертикально, затем координаты считывают по строкам, далее координаты преобразуются в буквы по этому же квадрату"

    @member
    class Method_three:
        """
        Усложнённая интерполяция координат.

        Усложнённый вариант, который заключается в следующем: полученный первичный шифротекст (После второго метода шифрования, цифровой) шифруется вторично. При этом он выписывается без разбиения на пары. Полученная последовательность цифр сдвигается циклически влево на один шаг (нечётное количество шагов, т.е. цифра 3 перемещается в конец). Эта последовательность вновь разбивается в группы по два и по таблице заменяется на окончательный шифротекст.

        Attributes:
            id (int): id метода.
            name (str): Название метода.
            description (str): Описание метода."""
        id: int = 3
        name: str = "Advanced Coordinates interpolation"
        desctiption: str = "Усложнённый вариант, который заключается в следующем: полученный первичный шифротекст (После второго метода шифрования, цифровой) шифруется вторично. При этом он выписывается без разбиения на пары. Полученная последовательность цифр сдвигается циклически влево на один шаг (нечётное количество шагов, т.е. цифра 3 перемещается в конец). Эта последовательность вновь разбивается в группы по два и по таблице заменяется на окончательный шифротекст."

class Cipher:
    def __init__(self):
        self.polubius_square: list[list] = []
        self.generated_alphabet: dict = {}
        self.alphabet: list = []
        self.positions: list = []
        self.square_size: dict[str, int]
        self.key: str = ""
        self.crypted_word = ""
        self.seed = 0

    def set_alphabet(self, alphabet: Alphabets.Types) -> None:
        self.alphabet = alphabet.value

    def set_size(self, square_size: Alphabets.Sizes) -> None:
        if not self.alphabet:
            raise ValueError("Чтобы указать размер квадрата, сначала укажите алфавит")
        else:
            self.square_size = square_size.value

    def set_key(self, key: str) -> None:
        if len(key) <= self.square_size["x_size"]:
            self.key = key
        else:
            raise ValueError(
                "Длина ключа для кириллицы не может быть больше 6-ти символов!"
            )

    def set_seed(self, seed: str):
        self.seed = seed
        random.seed(self.seed)

    def check_word(self, word: str):
        for char in word.lower():
            if char not in self.alphabet:
                raise(ValueError("В слове содержаться недопустимые символы"))

    def generate_positions(self):
        all_strings: list[str] = []
        used_strings = set()
        for i in range(self.square_size["y_size"]):
            for j in range(self.square_size["x_size"]):
                while True:
                    new_string = f"{secrets.SystemRandom().randint(1, self.square_size["y_size"])}{secrets.SystemRandom().randint(1, self.square_size["x_size"])}"
                    if new_string not in used_strings:
                        all_strings.append(new_string)
                        used_strings.add(new_string)
                        break
        self.positions = all_strings

    def _generate_alphabet(self):
        offset = 0
        for i in range(0, len(self.positions)):
            if self.alphabet[i] == "i":
                self.generated_alphabet[self.positions[i]] = "i/j"
                offset += 1
            else:
                self.generated_alphabet[self.positions[i]] = self.alphabet[i + offset]

    def _is_values_set(self) -> bool:
        if self.alphabet is None:
            raise (ValueError("Сначала укажите алфавит"))
        if self.square_size is None:
            raise (ValueError("Сначала укажите размер алфавита"))
        return True

    def create_square(self, shuffle_chars: bool = True):
        self._is_values_set()
        if shuffle_chars:
            self._generate_alphabet()
            for i in range(1, self.square_size["y_size"] + 1):
                self.polubius_square.append([i] * self.square_size["x_size"])

            for pos in self.generated_alphabet:
                self.polubius_square[int(pos[0]) - 1][int(pos[1]) - 1] = self.generated_alphabet[pos]
        else:
            for i in range(1, self.square_size["y_size"] + 1):
                self.polubius_square.append([i] * self.square_size["x_size"])
            offset = 0
            counter = 0
            for i in range(0, self.square_size["y_size"]):
                for j in range(0, self.square_size["x_size"]):
                    if self.alphabet[counter + offset] == "i":
                        self.polubius_square[i][j] = "i/j"
                        offset += 1
                    else:
                        self.polubius_square[i][j] = self.alphabet[counter + offset]
                    counter += 1

        print(self.generated_alphabet)

    #! ADD CHECK FOR SQUARE READY and etc.
    def crypt_word(self, word: str, method: Methods) -> str:
        self.check_word(word)
        self.crypted_word = ""

        if method == Methods.Method_one:
            for char in word.lower():
                for i in range(0, self.square_size["y_size"]):
                    for j in range(0, self.square_size["x_size"]):
                        if char in self.polubius_square[i][j].replace("/", ""):
                            if i+1 == self.square_size["y_size"]:
                                self.crypted_word += self.polubius_square[0][j]
                            else:
                                self.crypted_word += self.polubius_square[i+1][j]
        elif method == Methods.Method_two:
            new_postitions = []
            temp_positions = []
            for i in range(0, self.square_size["y_size"]):
                for j in range(0, self.square_size["x_size"]):
                    if self.polubius_square[j][i] in word:
                        temp_positions.append(f"{j}{i}")
            print(temp_positions)
            vertical_string = ""
            horizontal_string = ""
            for pos in temp_positions:
                vertical_string += pos[0]
                horizontal_string += pos[1]
            for ver, hor in zip((vertical_string + horizontal_string)[::2], (vertical_string + horizontal_string)[1::2]):
                new_postitions.append(f"{ver}{hor}")
            for i in range(0, self.square_size["y_size"]):
                for j in range(0, self.square_size["x_size"]):
                    if f"{j}{i}" in new_postitions:
                        self.crypted_word += self.polubius_square[j][i]
        elif method == Methods.Method_three:
            pass
        else:
            raise(ValueError("Недопустимый метод шифрования"))

word_to_crypt: str = "Iruma"

cipher = Cipher()
cipher.set_alphabet(Alphabets.Types.latin)
cipher.set_size(Alphabets.Sizes.Latin_Standard)
cipher.generate_positions()
cipher.create_square(True)
cipher.crypt_word(word_to_crypt, Methods.Method_two)

print(cipher.positions)

for i in range(0, len(cipher.polubius_square)):
    print("\n")
    for j in range(0, len(cipher.polubius_square[i])):
        print(cipher.polubius_square[i][j], end=" ")

print(f"\n\nСлово до шифровки: {word_to_crypt}\n\nСлово после шифровки: {cipher.crypted_word}")