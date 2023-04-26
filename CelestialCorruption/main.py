#Developed by Tyler Johnson and Kaine Clark

#credits to Kelvin Shadewing for sounds
#http://www.kelvinshadewing.net/


from scripts.game import *

def main():
    game = Game()
    game.start_Screen()
    while True:
        game.new()
        game.gameLoop()
        game.end_Screen()



if __name__ == '__main__':
    main()