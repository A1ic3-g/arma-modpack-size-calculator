import os
from bs4 import BeautifulSoup
from hurry.filesize import filesize

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
            print(fp)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


if __name__ == "__main__":

    # Get modpack path from user
    modpack_found = False
    while modpack_found == False: 
        # Get user input
        modpack_path = str(input("Enter path to modpack .html file: "))
        if os.path.exists(modpack_path):
            modpack_found = True 
        else:
            print("File not found, please try again")
    
    # Read modpack html file into a single string
    with open(modpack_path, 'r') as f:
        modpack_string =  f.read()

    # Parse the html string into a BeautifulSoup object
    html_soup = BeautifulSoup(modpack_string, 'html.parser')
    
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
        workshop_folder_path = str(input("Enter workshop folder path: "))

        if os.path.exists(workshop_folder_path) and os.path.dirname != "!WORKSHOP":
            workshop_folder_found = True 
        else:
            print("Invalid Folder path entered")
            print("please ensure you're NOT entering your !WORKSHOP folder path")
            print("A typical true workshop folder path looks like steamapps\workshop\content\\107410")

    # Get all the folder sizes
    total_size = 0
    mod_sizes = []
    for modpack_id in modpack_ids:
        mod_path = os.path.join(workshop_folder_path, modpack_id)
        size = get_size(start_path=mod_path)
        total_size += size
        mod_sizes.append(size)


    print(f"Traditional 1024 scale (used by windows): {filesize.size(total_size)}")
    print(f"SI 1000 scale: {filesize.size(total_size, system=filesize.si)}")