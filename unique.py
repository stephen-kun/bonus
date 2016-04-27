import random, string

def random_str(length=10):
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:length])

def random_digit(length=8):
    a = list(string.digits)
    random.shuffle(a)
    return ''.join(a[:length])

def create_primary_key(key='1', length=9):
    a = list(string.digits)
    random.shuffle(a)   
    primary = key + ''.join(a[:length])
    return string.atoi(primary, 10)



if __name__ == '__main__':
    for x in range(20):
        print(random_digit(12))
