from UI_element import DraggableUIElement
import pygame 

def create_ui_elements(canvas_x, canvas_y, canvas_width, canvas_height, ui_element_height, text_color=(255, 255, 255)):
    # Colors that match the personas exactly
    BROWN = (97, 62, 62)     # Adult
    ORANGE = (255, 98, 40)   # Child
    GREY = (150, 150, 150)   # Old Person
    
    ui_elements_color = [
        DraggableUIElement(705, 855, 150, 150, BROWN),      # Adult
        DraggableUIElement(1040, 855, 150, 150, ORANGE),     # Child
        DraggableUIElement(1372, 855, 150, 150, GREY)        # Old Person
    ]
    
    ui_elements_photo = [
        DraggableUIElement(705, 855, 150, 150, "assets/SuitcaseMoney.png"),
        DraggableUIElement(1040, 855, 150, 150, "assets/ToyCar.png"),
        DraggableUIElement(1372, 855, 150, 150, "assets/Gramophone.png")
    ]
    
    ui_elements_font = [
        DraggableUIElement(
            705, 855, 150, 150,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("timesnewroman", 100),
            font_name="timesnewroman",
            text_color=(255, 255, 255)  # White text
        ),
        DraggableUIElement(
            1040, 855, 150, 150,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("comicsansms", 100),
            font_name="comicsansms",
            text_color=(255, 255, 255)  # White text
        ),
        DraggableUIElement(
            1372, 855, 150, 150,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("brushscript", 130),
            font_name="brushscript",
            text_color=(255, 255, 255)  # White text
        )
    ]
    
    return ui_elements_color, ui_elements_photo, ui_elements_font