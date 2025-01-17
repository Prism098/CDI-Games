from UI_element import DraggableUIElement
import pygame 
def create_ui_elements(canvas_x, canvas_y, canvas_width, canvas_height, ui_element_height):
    ui_element_width = canvas_width // 3  # Divide the canvas into 3 equal sections for UI elements
    
    # Create a list of draggable elements with different colors (Round 1)
    ui_elements_color = [
        DraggableUIElement(270, 650, 125, 125, (77, 55, 50)),  # Example color (brownish)
        DraggableUIElement(590, 650, 125, 125, (255, 98, 40)),  # Example color (orange)
        DraggableUIElement(900, 650, 125, 125, (150, 150, 150)) # Example color (grey)
    ]
    
    # Create a list of draggable photo elements (Round 2)
    ui_elements_photo = [
        DraggableUIElement(270, 650, 125, 125, "assets/ProfessionalManPhoto.png"),  # Example photo (brownish)
        DraggableUIElement(590, 650, 125, 125, "assets/CartoonHappyPhoto.png"),  # Example photo (orange)
        DraggableUIElement(900, 650, 125, 125, "assets/OldManPhoto.png") # Example photo (grey)
    ]
    
    # Create a list of draggable font elements (Round 3)
    ui_elements_font = [
        DraggableUIElement(
           270, 650, 125, 125,
            color_or_image=None,  # We don't need color_or_image for font, it's not used in DraggableUIElement for text
            text="Aa",
            font=pygame.font.SysFont("timesnewroman", 50),
            font_name="timesnewroman",
        ),
        DraggableUIElement(
          590, 650, 125, 125,
            color_or_image=None,  # Again, no need for color_or_image
            text="Aa",
            font=pygame.font.SysFont("comicsansms", 50),
            font_name="comicsansms",
        ),
        DraggableUIElement(
            900, 650, 125, 125,
            color_or_image=None,  # Again, no need for color_or_image
            text="Aa",
            font=pygame.font.SysFont("couriernew", 50),
            font_name="couriernew",
        ),
    ]
    
    return ui_elements_color, ui_elements_photo, ui_elements_font
