from Bot import GameBot

def main():
    g = GameBot("Derp", (0, 255, 0))

    while input() != 'quit':
        pass

    g.close()
main()
