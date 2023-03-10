import os
from bs4 import BeautifulSoup
from hurry.filesize import filesize
import pygame
from classes import InputBox,Button

# substring of Steam workshop url that marks the start of the steam workshop ID
ID_START = '?id='

# Getsize courtesy of monkut on stackoverflow
# https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
def get_size(start_path = '.'):
    """Gets the size in bytes of a given file or folder (recursive)
        start_path = the path of the folder to get size of"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
                        # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def modpack__size(html_path,workshop_path):
    # Get modpack path from user
    modpack_found = False
    while modpack_found == False: 
        # Get user input
        modpack_path = html_path
        if os.path.exists(modpack_path):
            modpack_found = True 
        else:
            return("Modpack Error") # Return an error message
    
    # Read modpack html file into a single string
    with open(modpack_path, 'r') as f:
        # Parse the html string into a BeautifulSoup object
        html_soup = BeautifulSoup(f, 'html.parser')

    # Get mod IDs of all mods in the modpack
    modpack_ids = []
    for link in html_soup.find_all('a'):
        page = link.get('href')
        id_loc = page.find(ID_START)
        id = page[id_loc+len(ID_START):]
        modpack_ids.append(id)

    # Get workshop folder containing mods
    # Typically steamapps/workshop/content/107410
    # Note: this is NOT the !WORKSHOP folder 
    workshop_folder_found = False
    while workshop_folder_found == False:
        workshop_folder_path = workshop_path

        if os.path.exists(workshop_folder_path) and os.path.dirname != "!WORKSHOP":
            workshop_folder_found = True 
        else:
            return("Workshop Path Error") # Return an error message

    # Get all the folder sizes
    total_size = 0
    mod_sizes = []
    for modpack_id in modpack_ids:
        mod_path = os.path.join(workshop_folder_path, modpack_id)
        size = get_size(start_path=mod_path)
        total_size += size
        mod_sizes.append(size)

    return(filesize.size(total_size),filesize.size(total_size,system=filesize.si)) 

# PYGAME GUI SECTION

# Window dimensions in pixel units.
WIDTH,HEIGHT=800,600

input_text = '' # Holds text which is being input
pygame.init() # Initialises the pygame window as well as other fun variables and stuff that pygame needs to keep track of whats going on

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT)) # Starts display with correct size

text_font = pygame.font.Font('font/C&C Red Alert [INET].ttf',22) # Defines a font for use later

# Instantiation of the visual elements
htmlbox = InputBox(SCREEN,600,(178, 247, 239),(123, 223, 242),[50,100],text_font)
workshopbox = InputBox(SCREEN,600,(247, 214, 224),(242, 181, 212),[50,300],text_font)
confirmbutton = Button(SCREEN,50,120,(0, 108, 103),"Click to run",text_font,[400,500])

# Used to keep track of the state of the program (changed when button is pressed)
completion_state = 0
# 0 = No output (Default at start)
# 1 = Correct output -> Display size values
# 2 = HTML File is wrong error
# 3 = Modpack folder is wrong error

# PYGAME EVENT LOOP
not_finished = True
while not_finished:
    for event in pygame.event.get(): # Event Loop
        if event.type == pygame.QUIT:
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN: # On mouse press
            # Checks if mouse collides with any buttons/textboxes
            mouse_x,mouse_y = pygame.mouse.get_pos()
            
            # Checks collisions
            if htmlbox.get_rect().collidepoint(mouse_x,mouse_y): 
                htmlbox.set_selected(True)
                workshopbox.set_selected(False)
            
            elif workshopbox.get_rect().collidepoint(mouse_x,mouse_y):
                workshopbox.set_selected(True)
                htmlbox.set_selected(False)
            
            elif confirmbutton.get_rect().collidepoint(mouse_x,mouse_y):
                values = modpack__size(htmlbox.get_text(),workshopbox.get_text())
                if isinstance(values,tuple): # If succesful values got passed back, it'll be a tuple, else it'll be an error string
                    completion_state = 1
                elif values == "Modpack Error": # HTML is wrong
                    completion_state = 2
                elif values == "Workshop Path Error": # Modpack is wrong
                    completion_state = 3


            else: # Clicking outside any buttons/textboxes will unselect all. 
                htmlbox.set_selected(False)
                workshopbox.set_selected(False)
                input_text = ""
                
        # Typing events
        if event.type == pygame.KEYDOWN:
            if htmlbox.get_selected():
                if event.key == pygame.K_BACKSPACE: # To delete characters
                    input_text = input_text[0:-1]
                else: # Add input to string
                    input_text += event.unicode
                htmlbox.set_text(input_text)
            
            if workshopbox.get_selected():
                if event.key == pygame.K_BACKSPACE: # To delete characters
                    input_text = input_text[0:-1]
                else: # Add input to string
                    input_text += event.unicode
                workshopbox.set_text(input_text)
            
    # SCREEN RENDERING
              
    SCREEN.fill((209, 217, 216))
    
    text_surface = text_font.render("HTML file Path:",False,(0,0,0))
    SCREEN.blit(text_surface,(50,80))

    text_surface = text_font.render("Modpack folder Path:",False,(0,0,0))
    SCREEN.blit(text_surface,(50,280))


    if completion_state == 1:
        
        text_surface = text_font.render(f"Sizes:",False,(0,0,0))
        SCREEN.blit(text_surface,(70,380))
        text_surface = text_font.render(f"Traditional 1024 Scale(Used by windows): {values[0]}",False,(0,0,0))
        SCREEN.blit(text_surface,(70,400))
        text_surface = text_font.render(f"1000 SI Scale: {values[1]}",False,(0,0,0))
        SCREEN.blit(text_surface,(70,420))
    
    elif completion_state == 2:
        text_surface = text_font.render("Modpack HTML File path wrong",False,(0,0,0))
        SCREEN.blit(text_surface,(70,380))
    
    elif completion_state == 3:
        text_surface = text_font.render("Modpack folder path wrong",False,(0,0,0))
        SCREEN.blit(text_surface,(70,380))        


    htmlbox.update()
    workshopbox.update()
    confirmbutton.update()
    
    pygame.display.update()

    

