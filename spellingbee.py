import pandas as pd
import os
import datetime
import time
import argparse
import matplotlib.pyplot as plt

def root_dir():
    return os.path.dirname(os.path.abspath(__file__))

def showlog():
    log = pd.read_csv(os.path.join(root_dir(),"log.csv"), index_col="date")
    log.index = pd.to_datetime(log.index)
    plt.style.use('ggplot')
    print(log.tail(10))
    log.pecentage.plot(marker="o",title="Progress")
    plt.show()
    

class Spelling():
    """
    Spelling app
    """
    def __init__(self, num=25, skip_intro=False, words_file=os.path.join(root_dir(),"words.txt")):
        self._skip_intro = skip_intro
        self._num= num
        self._data = pd.read_csv(words_file, delimiter=",", header=None)
        self._log = pd.read_csv(os.path.join(root_dir(),"log.csv"))
        

    def _get_data(self):
        self.sample_data  = self._data.sample(self._num)

    def _say(self, sentence, sleepseconds=0.5):
        os.system("say {0}".format(sentence))
        time.sleep(sleepseconds)

    def _intro(self):
        self._say("Welcome to spelling bee. Please listen to the instructions ")
        self._say("Press n for next word")
        self._say("Press r for repeat")
        self._say("Press i for repeating this Instructions")

    def _show_words(self):
        print("\n")
        print("*"*50)
        for word in self.sample_data.values[:self._count+1]:
            for letter in word[0].upper():
                print (" ", letter,end="")
            print ("")
        print("*"*50)

    def _say_question(self, word):
        self._say(word)
        self._say("The word is {}".format(word))

    def _announce_left(self):
        num = self._count % 5
        if num != 0: 
            return
        self._say("Good work, {} more words to go!".format(self._num-self._count))

    def log(self):
        last_row, _ = self._log.shape
        self._say("Goodjob! How many words did you get correct")
        no_correct = input("Enter no of correct: ")
        percent = 100.0 * (float(no_correct)/ (self._count))
        self._log.loc[last_row+1] = [datetime.datetime.today()] + [percent]+[no_correct]+[self._count]
        self._log.to_csv("log.csv", index=False)
        
    def run(self):
        self._get_data()
        self._count = 0
        if not self._skip_intro:
            self._intro()

        
        while (self._count < self._num):
            self._say_question(self.sample_data.iloc[self._count,0])
            ans = input()
            ans = str(ans).lower()
            if 'n' == ans:
                self._count = self._count +1
            elif 'r' == ans:
                self._say_question(self.sample_data.iloc[self._count,0])
            elif 'i' == ans:
                self._intro()
            elif 'q' == ans:
                self._count = self._count +1
                break
            self._announce_left()
        self._say("Check your answers with the words below")
        self._show_words()
        self.log()


def main():
    parser = argparse.ArgumentParser(description="Spelling BEE")
    parser.add_argument("-num", type=int, default=15, help="number of words")
    parser.add_argument("-s","--skip-intro", action="store_true", help="Say intro")
    parser.add_argument("-w","--word-file", nargs=1, default=os.path.join(root_dir(),"words.txt"))
    args = parser.parse_args()
    gui=Spelling(num=args.num, skip_intro=args.skip_intro, words_file=args.word_file[0])
    gui.run()

if __name__ =="__main__":
    main()