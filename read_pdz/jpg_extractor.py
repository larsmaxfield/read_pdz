# AUTOGENERATED! DO NOT EDIT! File to edit: ../notebooks/20_extracting-image-data.ipynb.

# %% auto 0
__all__ = ['extract_jpg']

# %% ../notebooks/20_extracting-image-data.ipynb 12
from . import file_to_bytes, get_blocks, get_blocktypes 
import numpy as np 
import io 
import re
import matplotlib.pyplot as plt 
from PIL import Image

# %% ../notebooks/20_extracting-image-data.ipynb 13
def extract_jpg(pdz_file, BLOCKTYPE=137, save_file=False): 
    '''Extract jpg image from `pdz_file`.'''
    
    # parse into blocks 
    pdz_bytes = file_to_bytes(pdz_file)
    block_list = get_blocks(pdz_bytes, verbose=False)

    # read block 137 (if present)
    blocktypes_list = get_blocktypes(block_list)

    if BLOCKTYPE not in blocktypes_list: 
        print(f'Could not find jpg image data in: {pdz_file}')

    else: 
        jpg_i = blocktypes_list.index(137)
        jpg_dict = block_list[jpg_i]
        jpg_sandwich = jpg_dict['bytes'].tobytes()
    
        jpg_start = re.search(b'\xff\xd8', jpg_sandwich).span()[0]
        jpg_end = re.search(b'\xff\xd9', jpg_sandwich).span()[1]
        jpg = jpg_sandwich[jpg_start:jpg_end]
    
        im = np.array(Image.open(io.BytesIO(jpg))) 

        if save_file is True: 
            jpg_file = re.sub('\.pdz$', '.jpg', pdz_file) 
            print(f"Saving image file: '{jpg_file}'")
            plt.imsave(jpg_file, im) 

        return im 

    return None 