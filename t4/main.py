from Bot import GameBot

def main():
    g = GameBot("PyBot", (255, 0 ,0))

    while input() != 'quit':
        pass

    g.close()
main()
