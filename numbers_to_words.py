import sys
import threading
from decimal import Decimal, ROUND_HALF_UP


class NumberTranslator:
    __instance = None
    __allow_creation = False
    __instance_lock = threading.Lock()

    def __init__(self):
        if not NumberTranslator.__allow_creation:
            raise RuntimeError("This class is a singleton! Use get_instance() method to get the instance.")

        self.__number_mapping = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
            11: "eleven",
            12: "twelve",
            13: "thirteen",
            14: "fourteen",
            15: "fifteen",
            16: "sixteen",
            17: "seventeen",
            18: "eighteen",
            19: "nineteen",
            20: "twenty",
            30: "thirty",
            40: "forty",
            50: "fifty",
            60: "sixty",
            70: "seventy",
            80: "eighty",
            90: "ninety",
        }

        self.__power_mapping = {
            1: "thousand",
            2: "million",
            3: "billion",
            4: "trillion",
            5: "quadrillion",
            6: "quintillion",
            7: "sextillion",
            8: "septillion",
            9: "octillion",
            10: "nonillion",
            11: "decillion",
            12: "undecillion",
            13: "duodecillion",
            14: "tredecillion",
            15: "quattuordecillion",
        }

    @staticmethod
    def get_instance():
        if NumberTranslator.__instance is None:
            with NumberTranslator.__instance_lock:
                if NumberTranslator.__instance is None:
                    NumberTranslator.__allow_creation = True
                    NumberTranslator.__instance = NumberTranslator()
                    NumberTranslator.__allow_creation = False
        return NumberTranslator.__instance

    def get_word(self, number):
        return self.__number_mapping.get(number, "Number not found")

    def get_power_word(self, number):
        return self.__power_mapping.get(number, "Number not found")



def _validate_non_negative_int(value, name="number"):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be a non-negative integer.")
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


def _validate_non_negative_decimal(value, name="amount"):
    try:
        number = Decimal(str(value))
    except Exception as exc:
        raise ValueError(f"{name} must be a valid non-negative number.") from exc

    # Check for NaN and Infinity
    if number.is_nan() or number.is_infinite():
        raise ValueError(f"{name} must be a finite number.")

    if number < 0:
        raise ValueError(f"{name} must be non-negative.")


def convert_to_float_text(str_float_number):
    _validate_non_negative_decimal(str_float_number, "amount")

    amount = Decimal(str_float_number).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    int_part = int(amount)
    cents_value = int((amount - Decimal(int_part)) * 100)

    if cents_value == 100:
        int_part += 1
        cents_value = 0

    return int_part, cents_value


def convert_to_float_text_with_currency(str_float_number):
    _validate_non_negative_decimal(str_float_number, "amount")

    int_part, cents_value = convert_to_float_text(str_float_number)

    answer = convert_to_text(int_part)

    if int_part == 1:
        answer += " dollar"
    else:
        answer += " dollars"

    if cents_value > 0:
        answer += " and " + convert_to_text(cents_value)
        if cents_value == 1:
            answer += " cent"
        else:
            answer += " cents"

    return answer


def convert_to_text(number):

    _validate_non_negative_int(number, "number")

    translator = NumberTranslator.get_instance()

    if number == 0:
        return translator.get_word(number)

    num_builder = []
    threes = (len(str(number)) - 1) // 3

    if threes > 15:
        raise ValueError(f"{number} too large to convert to text.")

    while threes >= 0:
        
        power_10 = 10 ** (threes * 3)
        working_set = (number // power_10) % 1000
        number %= power_10
        over = working_set % 100

        prefixed = 0

        if working_set > 99:
            num_builder.append(translator.get_word(working_set // 100))
            num_builder.append("hundred")
            prefixed = 1

        if over >= 20:
            if prefixed == 1:
                num_builder.append("and")
                prefixed |= 2

            unit = over % 10
            num_builder.append(translator.get_word((over // 10) * 10))
            prefixed |= 4
            over = unit

        if over > 0:

            if (prefixed & 4) == 4:
                num_builder.append("-")

            elif (prefixed & 1) == 1:
                num_builder.append("and")

            num_builder.append(translator.get_word(over))

            prefixed |= 8

        if threes > 0 and prefixed > 0:
            num_builder.append(translator.get_power_word(threes))

        threes -= 1

    number = " ".join([word for word in num_builder if word])
    number = number.replace(" - ", "-")

    return number


def convert_to_text_with_currency(number):
    _validate_non_negative_int(number, "number")

    number_as_text = convert_to_text(number)

    if number == 1:
        number_as_text += " dollar"
    else:
        number_as_text += " dollars"

    return number_as_text


def main():
    if len(sys.argv) >= 2:
        str_number = sys.argv[1]

        if "." not in str_number:
            try:
                number = int(str_number)
                print(convert_to_text_with_currency(number))
            except (ValueError, TypeError):
                print("Please enter a valid positive number.")
        else:
            try:
                print(convert_to_float_text_with_currency(str_number))
            except (ValueError, TypeError):
                print("Please enter a valid positive number with a decimal point, if required.")
    else:

        
        numbers = [0, 1, 20, 31, 100, 156, 400, 820, 985, 1000, 1005, 12345, 100000, 800005, 2000005, 12345678, 9876543210, 1234567890, 1000000000000001, 90000000000000000000000000000000000000]
        float_numbers = ["0.", "1.5", "20.999", "31.95", "100.00", "156.58984", "400.336", "985.1", "1000.5", ".9876", "12345", "100000.012", "800005.106", "1000.", "1234567890987654321.111"]

        valid_answers = ["zero dollars",
                         "one dollar",
                         "twenty dollars",
                         "thirty-one dollars",
                         "one hundred dollars",
                         "one hundred and fifty-six dollars",
                         "four hundred dollars",
                         "eight hundred and twenty dollars",
                         "nine hundred and eighty-five dollars",
                         "one thousand dollars",
                         "one thousand five dollars", 
                         "twelve thousand three hundred and forty-five dollars",
                         "one hundred thousand dollars",
                         "eight hundred thousand five dollars", 
                         "two million five dollars",
                         "twelve million three hundred and forty-five thousand six hundred and seventy-eight dollars",
                         "nine billion eight hundred and seventy-six million five hundred and forty-three thousand two hundred and ten dollars",
                         "one billion two hundred and thirty-four million five hundred and sixty-seven thousand eight hundred and ninety dollars",
                         "one quadrillion one dollars",
                         "ninety undecillion dollars"]

        valid_float_answers = ["zero dollars",
                                "one dollar and fifty cents",
                                "twenty-one dollars",
                                "thirty-one dollars and ninety-five cents",
                                "one hundred dollars",
                                "one hundred and fifty-six dollars and fifty-nine cents",
                                "four hundred dollars and thirty-four cents",
                                "nine hundred and eighty-five dollars and ten cents",
                                "one thousand dollars and fifty cents",
                                "zero dollars and ninety-nine cents",
                                "twelve thousand three hundred and forty-five dollars",
                                "one hundred thousand dollars and one cent",
                                "eight hundred thousand five dollars and eleven cents",
                                "one thousand dollars",
                                "one quintillion two hundred and thirty-four quadrillion five hundred and sixty-seven trillion eight hundred and ninety billion nine hundred and eighty-seven million six hundred and fifty-four thousand three hundred and twenty-one dollars and eleven cents"]

        failures = 0
        numbers_in_words = [convert_to_text_with_currency(number) for number in numbers]
        counter = 1

        for i in range(len(numbers)):

            if (numbers_in_words[i] != valid_answers[i]):
                print(counter, "Test failed for ", numbers[i])
                print("Expected:", valid_answers[i], "but got:", numbers_in_words[i])
                failures += 1
            
            counter += 1

        float_numbers_in_words = [convert_to_float_text_with_currency(float_number) for float_number in float_numbers]
        counter = 1

        for i in range(len(float_numbers)):

            if (float_numbers_in_words[i] != valid_float_answers[i]):
                print(counter, "Test failed for ", float_numbers[i])
                print("Expected:", valid_float_answers[i], "but got:", float_numbers_in_words[i])
                failures += 1
            
            counter += 1


        counter = 0
        try:
           # 1 Too large of a number - integer
           invalid_number = convert_to_text(12345678901234567890123456789012345678901234567890)
           failures += 1

           print(counter, "Test failed for 12345678901234567890123456789012345678901234567890. Expected ValueError, it succeeded with this value:", invalid_number)

        except (ValueError, TypeError):
            counter += 1


        try:
           # 2 NaN input
           invalid_nan_number = convert_to_float_text_with_currency("NaN")
           failures += 1

           print(counter, "Test failed for NaN. Expected ValueError, it succeeded with this value:", invalid_nan_number)

        except (ValueError, TypeError):
            counter += 1


        try:
           # 3 Infinity Input
           invalid_infinity_number = convert_to_float_text_with_currency("Infinity")
           failures += 1

           print(counter, "Test failed for Infinity. Expected ValueError, it succeeded with this value:", invalid_infinity_number)

        except (ValueError, TypeError):
            counter += 1


        try:
           # 4 Negative number input
           invalid_negative_integer = convert_to_text(-100)
           failures += 1

           print(counter, "Test failed for Negative Integer. Expected ValueError, it succeeded with this value:", invalid_negative_integer)

        except (ValueError, TypeError):
            counter += 1


        try:
           # 4 Negative floating number input
           invalid_negative_float = convert_to_float_text(-21.22)
           failures += 1

           print(counter, "Test failed for Negative Float. Expected ValueError, it succeeded with this value:", invalid_negative_float)

        except (ValueError, TypeError):
            counter += 1   

        if failures == 0:
            print("All tests passed!")

if __name__ == "__main__":
    main()
