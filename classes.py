import pygame

# InputBox Class
#
# Used as a textbox for receiving user inputs


class InputBox():
    """
    InputBox Class

    Used for creating an box that stores and displays text input to it via the set_text() method.
    
    Parameters:
    INPUT
    - SCREEN = pygame.Surface that is used as the main display
    - length = Int determining the pixel length of the text box.
    - colour = pygame.Color representing a colour for the box
    - border_colour = pygame.Color which represents the border.
    - position = Array or tuple in format [int,int] which represents the top left pixel location which the input box is displayed from.
    - font = pygame.font.Font used to display the writing passed to it.
    
    - text = string which holds the string to be displayed on it as it is being typed.
    - rect = pygame.Rect holding the position 
    - is_selected = Bool used to determine whether to highlight the box as it is focused. 

    Methods:
    - __init__(SCREEN,length,colour,border_colour,position,font) = The constructor method
    - update() = To be called once per frame from the main loop to call the different visual parts to the screen to be displayed.
    - set_text(new_text) = Method used to update the input text that is to be displayed.
    - get_rect() = Function to get pygame.Rect of the object
    """


    def __init__(self,SCREEN:pygame.Surface,length:str,colour:pygame.Color,border_colour:pygame.Color,position:list|tuple,font:pygame.font.Font)->None:

        self.SCREEN = SCREEN
        self.length = length
        self.colour = colour
        self.border_colour = border_colour
        self.position = position
        self.font = font

        self.is_selected = False
        self.text = ''
        self.rect = pygame.Rect(position[0],position[1],length,50) # Defines a rectangle used mainly for collision detection

    def set_text(self,new_text):
        self.text = new_text
    
    def set_selected(self,value:bool):
        self.is_selected = value
    
    def get_rect(self)->pygame.Rect:
        return(self.rect)

    def get_selected(self)->bool:
        return(self.is_selected)

    def get_text(self)->str:
        return(self.text)
    
    def update(self):
        pygame.draw.rect(self.SCREEN,self.colour,self.rect)
        if self.is_selected:
            pygame.draw.rect(self.SCREEN,self.border_colour,self.rect,5)
        else:
            pygame.draw.rect(self.SCREEN,self.border_colour,self.rect,2)
        text_surface = self.font.render(self.text,False,(0,0,0))
        self.SCREEN.blit(text_surface,(self.position[0]+10,self.position[1]+20))        


# Button Class
#
# Used to send a signal to the program via click

class Button():
    """
    Button Class

    A simple object that is supposed to look like a button (Has no function)
    
    Parameters:
    INPUT
    - SCREEN = pygame.Surface that is used as the main display
    - height = Int determining pixel height of button.
    - width = Int determining pixel width of the button.
    - colour = pygame.Color representing a colour for the box
    - text = Str Determines the text displayed in the middle of the button.
    - font = pygame.font.Font used to display the writing passed to it.
    - position = Array or tuple in format [int,int] which represents the top left pixel location which the input box is displayed from.
    
    
    - rect = pygame.Rect holding the position / dimensions

    Methods:
    - __init__(SCREEN,height,width,colour,text,font,position) = The constructor method
    - update() = To be called once per frame from the main loop to call the different visual parts to the screen to be displayed.
    - get_rect() = Function to get pygame.Rect of the object
    """
    def __init__(self, SCREEN:pygame.Surface,height:int,width:int,colour:pygame.Color,text:str,font:pygame.font.Font,position:list|tuple)->None:
        
        self.SCREEN = SCREEN
        self.height = height
        self.width = width
        self.colour = colour
        self.text = text
        self.font = font
        self.position = position
        
        self.rect = pygame.Rect(self.position[0],self.position[1],width,height) # Rectangle used for collision detection

    def get_rect(self)->pygame.rect.Rect:
        return(self.rect)

    def update(self):
        pygame.draw.rect(self.SCREEN,self.colour,self.rect)
        text_surface = self.font.render(self.text,False,(0,0,0))
        self.SCREEN.blit(text_surface,(self.position[0]+10,self.position[1]+(self.height//4)))

