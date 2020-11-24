from gi.repository import Clutter

# Initialise
Clutter.init()

# Create the stage
stage = Clutter.Stage()
stage.set_background_color(Clutter.color_from_string("Red")[1])
stage.set_size(400,400)
stage.set_title("Hello World 7")

# Get ready to start
stage.show_all()
Clutter.main()



