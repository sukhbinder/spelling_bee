import pandas as pd
import os
import datetime
import time
import argparse
import matplotlib.pyplot as plt
import sys
import pygame

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
        if sys.platform.startswith('linux'):
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(sentence)
            engine.setProperty('rate',90)
            engine.setProperty('volume', 0.9)
            engine.runAndWait()
        elif sys.platform.startswith('darwin'):
            os.system("say {0}".format(sentence))
        time.sleep(sleepseconds)

    def _intro(self):
        self._say("Welcome to spelling bee. Please listen to the instructions ")
        self._say("A word will be read, try to spell it ")
        self._say("Once you have typed it in, press enter, and then either ")
        self._say("Press n for next word and press enter ")
        self._say("Press r and enter to hear the word again ")
        self._say("Press i and enter to repeating these instructions ")
        self._say("Press q and enter to quit")

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
        self._say("Goodjob! How many words did you get correct?")
        no_correct = input("Enter the number of correct words: ")
        percent = 0
        if self._count:
            percent = 100.0 * (float(no_correct)/ (self._count))
        self._log.loc[last_row+1] = [datetime.datetime.today()] + [percent]+[no_correct]+[self._count]
        self._log.to_csv("log.csv", index=False)
        
    def run(self):
        self._get_data()
        self._count = 0
        if not self._skip_intro:
            self._intro()
        print("\nr for repeat, n for next word, q to quit\n")

        
        while (self._count <= self._num):
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
                break
            self._announce_left()
        self._say("Check your answers with the words below")
        self._show_words()
        pygame.mixer.init(44100,-16,2,2048)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.load('music/Bhangra.mid')
        pygame.mixer.music.play()
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
