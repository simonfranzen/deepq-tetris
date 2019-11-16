import os.path

class Plotter:

    def __init__(self, number):
        self.file_name = 'data/train/highscore-{}'.format(number)
        if not os.path.exists(self.file_name):
            self.reset()


    def write(self, data):
        file = open(self.file_name, 'a+')
        file.write('{}\n'.format(data))
        file.close()


    def reset(self):
        file = open(self.file_name, 'w+')
        file.write('')
        file.close()

