class Fire:
    size = 0
    temp = 0
    type = 'dragon'

    def __init__(self, size, temp, type):
        self.size = size
        self.temp = temp
        self.type = type


if __name__ == '__main__':
    Fireball = Fire(size=50,temp=200,type='phoenix')
    print(str(Fireball.type) + " fire fireball technique is used!")