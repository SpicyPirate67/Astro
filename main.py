
import Galaxy_Class

json_path = "/home/spicypirate/Documents/Uni/Astro Assignment/code/Skyserver_SQL11_9_2022 5 24 24 PM.json"
img_path = "/home/spicypirate/Documents/Uni/Astro Assignment/code/images/"

galaxy = Galaxy_Class.Galaxy(False, False, True, json_path, img_path)
galaxy.func()
galaxy.drawPlot()