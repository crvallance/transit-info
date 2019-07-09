import time
import board
from adafruit_pyportal import PyPortal
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

cwd = ("/"+__file__).rsplit('/', 1)[0]
names_font =  bitmap_font.load_font(cwd+"/fonts/Helvetica-Bold-16.bdf")
# pre-load glyphs for fast printing
names_font.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ- ()')
names_position = (10, 135)
names_color = 0xFF00FF


# determine the current working directory needed so we know where to find files
cwd = ("/"+__file__).rsplit('/', 1)[0]
pyportal = PyPortal(status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/tracker-bg.bmp",
                    image_position=(0, 0),
                    caption_font=cwd+"/fonts/Helvetica-Bold-100.bdf",
                    #caption_text='Hello dere',
                    #caption_position=(0, 0),
                    #caption_color=0x808000)
)

while True:
    response = None
    try:
        names_textarea = Label(names_font, text='woo')
        names_textarea.x = names_position[0]
        names_textarea.y = names_position[1]
        names_textarea.color = names_color
        pyportal.splash.append(names_textarea)
    except (ValueError, RuntimeError) as e:
        print("failed to send data..retrying...")
