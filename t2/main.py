from map_loader import MapLoader
from gui import Gui
from prolog import PrologActor

def update_map():
    pl.atualiza()
    gui.set_map_actor(pl.mapa)

# Program entry point
map_full = MapLoader("mapa.txt").mapa
pl = PrologActor("teste.pl")
gui = Gui(update_map)
gui.set_map_full(map_full)
#gui.set_map_actor(map_full)
gui.start_draw_loop()
