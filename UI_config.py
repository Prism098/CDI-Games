from UI_element import DraggableUIElement
import pygame 

def create_ui_elements(canvas_x, canvas_y, canvas_width, canvas_height, ui_element_height):
    # Colors that match the personas exactly
    BROWN = (77, 55, 50)     # Adult
    ORANGE = (255, 98, 40)   # Child
    GREY = (150, 150, 150)   # Old Person
    
    ui_elements_color = [
        DraggableUIElement(270, 650, 125, 125, BROWN),      # Adult
        DraggableUIElement(590, 650, 125, 125, ORANGE),     # Child
        DraggableUIElement(900, 650, 125, 125, GREY)        # Old Person
    ]
    
    ui_elements_photo = [
        DraggableUIElement(270, 650, 125, 125, "assets/SuitcaseMoney.png"),
        DraggableUIElement(590, 630, 125, 150, "assets/ToyCar.png"),
        DraggableUIElement(900, 650, 125, 125, "assets/Gramophone.png")
    ]
    
    ui_elements_font = [
        DraggableUIElement(
            270, 650, 125, 125,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("timesnewroman", 50),
            font_name="timesnewroman"
        ),
        DraggableUIElement(
            590, 650, 125, 125,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("comicsansms", 50),
            font_name="comicsansms"
        ),
        DraggableUIElement(
            900, 650, 125, 125,
            color_or_image=None,
            text="Aa",
            font=pygame.font.SysFont("brushscript", 50),
            font_name="brushscript"
        )
    ]
    
    return ui_elements_color, ui_elements_photo, ui_elements_font