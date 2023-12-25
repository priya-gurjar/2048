def get_digits_of_number(number):
    digits = []
    while number > 0:
        digits.append(number % 10)
        number //= 10
    return len(digits)
