from UI_element import DraggableUIElement

def create_ui_elements(canvas_x, canvas_y, canvas_width, canvas_height, ui_element_height):
    ui_element_width = canvas_width // 3  # Divide the canvas into 3 equal sections for UI elements
    
    # Create a list of draggable elements with different colors
    ui_elements = [
        DraggableUIElement(270, 650, 125, 125, (77, 55, 50)),  # Example color (brownish)
        DraggableUIElement(590, 650, 125, 125, (255, 98, 40)),  # Example color (orange)
        DraggableUIElement(900, 650, 125, 125, (150, 150, 150)) # Example color (grey)
    ]
    
    return ui_elements
