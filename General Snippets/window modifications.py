import pywinauto
import win32gui



def draw_outline(element):
    """Draws a red outline around the specified window element."""

    # Get the bounding rectangle of the element
    rect = element.rectangle()

    # Get the device context for the desktop
    hdc = win32gui.GetDC(0)

    # Create a pen for drawing the outline
    pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(255, 0, 0))

    # Select the pen into the device context
    old_pen = win32gui.SelectObject(hdc, pen)

    # Draw the rectangle
    win32gui.Rectangle(hdc, rect.left, rect.top, rect.right, rect.bottom)

    # Restore the old pen
    win32gui.SelectObject(hdc, old_pen)

    # Delete the pen
    win32gui.DeleteObject(pen)

    # Release the device context
    win32gui.ReleaseDC(0, hdc)

# Example usage:
app = pywinauto.Application(backend="uia").start("notepad.exe")
dlg = app.Notepad
element = dlg.Edit

# Draw outline around the Notepad edit control
draw_outline(element)


#---------------------------------------------------------------------------------
'''
import pywinauto

app = pywinauto.Application().connect(title="Calculator")
window = app.top_window()
window.draw_outline(colour='red', thickness=50)
'''