import pygame
from enum import Enum 
from typing import Tuple

WHITE = (0,0,0)

# ----------------------------------------------------------------
# TextAlignment - text alignment is how to position text in a rectangle
# ----------------------------------------------------------------
class TextAlignment(Enum):
    Left = -1,
    Center = 0,
    Right = 1

Background = Tuple[pygame.Color, pygame.Surface, tuple, str]

# ----------------------------------------------------------------
# Render Utilites
# ----------------------------------------------------------------
def create_surface(width: int, height: int, background: Background) -> pygame.Surface:
    "create a new filled surface. background is either a color or an image path"
    if type(background) == pygame.Color or type(background) == tuple:
        surface = pygame.Surface((width, height))
        surface.fill(background)
    elif type(background) == str:
        image = pygame.image.load(background)
        r = image.get_rect()
        scale_x, scale_y = width / r.width, height / r.height 
        surface = pygame.transform.smoothscale_by(image, (scale_x, scale_y))
    elif type(background) == pygame.Surface:
        r = background.get_rect()
        scale_x, scale_y = width / r.width, height / r.height 
        surface = pygame.transform.smoothscale_by(background, (scale_x, scale_y))
    else:
        raise Exception(f"Unexpected type: {type(background)}")
    return surface


def render_text(image: pygame.Surface, text: str, color: pygame.Color, *,
                alignment = TextAlignment.Center, padding=10, size=48, 
                background: Background = WHITE) -> Tuple[int,int]:
    "renders a text string on a surface, returns size of text"
    font = pygame.font.SysFont(None, size)
    txt_image = font.render(text, True, color)

    r = txt_image.get_bounding_rect()
    txt_width, txt_height = r.width, r.height

    if image == None:
        # if no image provided, make it sized based of the text
        loc = (padding, padding)
        image = create_surface(txt_width + padding*2, txt_height + padding*2, background=background)
    elif alignment == TextAlignment.Left:
        loc = (padding,padding)
    elif alignment == TextAlignment.Center:
        img_width = image.get_bounding_rect().width
        loc = ((img_width - txt_width)//2, padding)
    elif alignment == TextAlignment.Right:
        img_width = image.get_bounding_rect().width
        loc = (img_width - txt_width - padding, padding)
    else:
        raise Exception(f"Unexpected TextAlignment: {alignment}")

    image.blit(txt_image, loc)
    
    return (txt_width, txt_height)

def render_border(image: pygame.Surface, border_width: int, border_color: pygame.Color) -> None:
    "render a border on a surface"
    if border_width > 0:
        pygame.draw.rect(image, border_color, image.get_rect(), width=border_width)
    
