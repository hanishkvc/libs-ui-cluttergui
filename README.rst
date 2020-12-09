#############################
A Simple ClutterGUI library
#############################
Author: HanishKVC
Version: 20201130IST0506

This is a simple gui library built using clutter, along with test applications which uses it.

This was created to checkout the clutter library.

It provides some simple widgets like a Label, TextButton, ImageButton, ListBox (of text/image buttons).

It supports scrolling of the listbox and itemclick call back.

It allows Listbox within ListBox and both Horizontal and Vertical scroll across them, as required,
when one of them is horizontal and the other vertical wrt orientation. One needs to press any mouse btn
and then drag it around as required, to trigger the scroll.

Look into the git log -p to get a fair idea of how to use clutter from python, as well as to
get a decent view of how this code was developed, with all the trials and errors if any inbtw.

One of the test apps, also provides a simple content browser similar to what one sees on Media streaming
platforms and or similar to what some of my products used to provide in general. This app even thou pretty
basic is fully themable. The theming and content data are both picked from text files which define the ui
template and or content meta data, as the case may be.

TODO:

Moving mouse beyond the ListBox's area will lead to any applied blur effect to persist beyond
the scroll. One needs to use a timeout logic to clear the blur effect if any applied during
scroll. [DONE]

Look into Custom Effects and possible issue with cogl.material wrt gi based Clutter and python later.

Mouse and Keyboard based scrolling dont play nice with one another properly currently, this
needs to be fixed later.


