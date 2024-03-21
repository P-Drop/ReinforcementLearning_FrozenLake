from enum import Enum
import os

# Window size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Colors
class Color(Enum):
    
    SIENNARED = (142, 55, 46)

    MIDNIGHTBLUE = (25,25, 112) #NO se usa
    DARKSLATEBLUE = (72, 61, 139)
    LIGHTSKYBLUE = (135,206,250)

    SELECTIVEYELLOW = (255, 191, 0)

    WHITE = (224,224,224)
    BLACK = (64,64,64)
    DARKERBLACK = (20, 20, 20)

# Box
BOX_SIZE = 200

# Fonts
fonts_path = 'fonts/'
class MyFonts(Enum):
    ROBOTO_BOLD = os.path.join(fonts_path, 'Roboto-Bold.ttf')
    SIGNATRA = os.path.join(fonts_path, 'Signatra.ttf')

# Images
img_path = 'img/'
class ImgPath(Enum):
    NUCLIO_FAVICON = os.path.join(img_path, 'nuclioFavicon.png')
    NUCLIO_DS = os.path.join(img_path, 'nuclio-digital-school-logo.webp')
    ICE = os.path.join(img_path, 'crack_ice.png')
    SEISITO = os.path.join(img_path, 'seisito.png')
    OPEN_CHEST = os.path.join(img_path, 'openChest.png')
    CLOSE_CHEST = os.path.join(img_path, 'closeChest.png')

# Sounds