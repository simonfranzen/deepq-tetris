import os.path

def sortSecond(val): 
    return val[1]

class Highscore:

    def __init__(self):
        self.file_name = 'data/highscore'
        if not os.path.exists(self.file_name):
            self.reset()


    def __str__(self):
        lines = []
        lines.append('\nHIGHSCORE')
        file = open(self.file_name, 'r')
        scores = []
        with open(self.file_name) as fp:
            for cnt, line in enumerate(fp):
                hs = line.replace(" ", "").strip().split('\t')
                scores.append([hs[0], int(hs[1])])
            
        file.close()
        scores.sort(key=sortSecond, reverse=True)
        rank = 1
        for name, score in scores:
            lines.append('Rank #{0} \t Name: {1} \t Points: {2}'.format(rank, name, score))
            rank += 1


        return '\n'.join(lines)


    def write(self, score):
        input('Press Enter to add to highscore')
        name = input('Enter your name:')
        file = open(self.file_name, 'a+')
        file.write('{0} \t {1} \n'.format(name, score))
        file.close()


    def reset(self):
        file = open(self.file_name, 'w+')
        file.write('')
        file.close()

