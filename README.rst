#############################
A Simple ClutterGUI library
#############################
Author: HanishKVC
Version: 20201130IST0506

This is a simple gui library built using clutter, along with a test application which uses it.

This was created to checkout the clutter library.

It provides some simple widgets like a Label, ImageButton, ListBox (of image buttons).

It supports scrolling of the listbox and itemclick call back.

Look into the git log -p to get a fair idea of how to use clutter from python, as well as to
get a decent view of how this code was developed, with all the trials and errors if any inbtw.

TODO:

Moving mouse beyond the ListBox's area will lead to any applied blur effect to persist beyond
the scroll. One needs to use a timeout logic to clear the blur effect if any applied during
scroll. [DONE]

Look into Custom Effects and possible issue with cogl.material later.

Mouse and Keyboard based scrolling dont play nice with one another properly currently, this
needs to be fixed later.


