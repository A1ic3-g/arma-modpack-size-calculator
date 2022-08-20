import os
from bs4 import BeautifulSoup
from hurry.filesize import filesize
import pandas

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
        # Parse the html string into a BeautifulSoup object
        html_soup = BeautifulSoup(f, 'html.parser')


    # Setup pandas dataframe to store modpack info
    modpack_df = pandas.DataFrame(columns=['ID', 'Name', 'Size'])

    # Get mod IDs of all mods in the modpack
    for mod in html_soup.find_all('tr'):

        # Get the Name of the mod
        mod_name_td = mod.find('td', {'data-type': 'DisplayName'})
        mod_name = mod_name_td.get_text()

        # Get the ID of the mod
        page = mod.find('a').get('href')
        id_loc = page.find(ID_START)
        id = page[id_loc+len(ID_START):]

        # Append to modpack_df using pd.concat()
        modpack_df = pandas.concat([modpack_df, pandas.DataFrame(data={'ID': [id], 'Name': [mod_name], 'Size': [0]})], ignore_index=True)

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

    print(modpack_df)
    # Get all the folder sizes
    total_size = 0
    for row in modpack_df.iterrows():
        mod_row = row[1]

        print(mod_row)
        mod_path = os.path.join(workshop_folder_path, mod_row['ID'])
        size = get_size(start_path=mod_path)
        total_size += size
        
        # insert size into dataframe for current mod
        modpack_df.loc[mod_row.name, 'Size'] = size


    print(f"Traditional 1024 scale (used by windows): {filesize.size(total_size)}")
    print(f"SI 1000 scale: {filesize.size(total_size, system=filesize.si)}\n")

    modpack_df.sort_values(by='Size', ascending=False, inplace=True)
    modpack_df['Size'] = modpack_df['Size'].apply(lambda x: x/1024**2)

    with pandas.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(modpack_df)