import os.path

class Plotter:

    path='data/train'

    def __init__(self, number):
        self.file_name = self.path+'game_results_{}'.format(number)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
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

