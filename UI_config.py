from UI_element import DraggableUIElement
import pygame 

def create_ui_elements(canvas_x, canvas_y, canvas_width, canvas_height, ui_element_height):
    # Colors that match the personas exactly
    BROWN = (97, 62, 62)     # Adult
    ORANGE = (255, 98, 40)   # Child
    GREY = (150, 150, 150)   # Old Person
    
    ui_elements_color = [
        DraggableUIElement(425, 650, 125, 125, BROWN),      # Adult
        DraggableUIElement(735, 650, 125, 125, ORANGE),     # Child
        DraggableUIElement(1050, 650, 125, 125, GREY)        # Old Person
    ]
    
    ui_elements_photo = [
        DraggableUIElement(425, 650, 125, 125, "assets/SuitcaseMoney.png"),
        DraggableUIElement(735, 630, 125, 150, "assets/ToyCar.png"),
        DraggableUIElement(1050, 650, 125, 125, "assets/Gramophone.png")
    ]
    
    ui_elements_font = [
        DraggableUIElement(
            425, 630, 125, 125,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("timesnewroman", 100),
            font_name="timesnewroman"
        ),
        DraggableUIElement(
            735, 630, 125, 125,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("comicsansms", 100),
            font_name="comicsansms"
        ),
        DraggableUIElement(
            1050, 640, 125, 125,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("brushscript", 130),
            font_name="brushscript"
        )
    ]
    
    return ui_elements_color, ui_elements_photo, ui_elements_font