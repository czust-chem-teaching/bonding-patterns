import numpy as np
import matplotlib.pyplot as plt
import argparse
import string
import networkx as nx
from PIL import Image
from matplotlib.colors import ListedColormap

temp=[]

colors = ['green', 'blue', 'orange', 'black']

cmap = ListedColormap(colors)


#draw the grid similar to the Periodic Table
grid = np.zeros([18, 18])
grid[0:1, 1:17] = 2
grid[1:3, 2:12] = 2
grid[10:18,0:18] = 2 
grid[5:7,2:3] =2# blank for lanthanoid and actinide 
grid[7:8,0:18] =2
grid[8:10,0:3]=2


#set the color scheme
plt.imshow(grid, cmap=cmap, interpolation='nearest')
#set the style of grid
plt.grid(True, which='both', color='black', linewidth=0.2)
#draw X and Y lables
plt.xticks(np.arange(-0.5, 18, 1),(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"]),fontsize=8)
plt.yticks(np.arange(-0.5, 18, 1),(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"]),fontsize=8)
#draw element name in each grid
with open("text-BE.txt","r") as filestream1:
  for line in filestream1:
    line1= line.strip('\n') 
    para=line1.split(",")
    a=para[2]+'\n'+para[3]
    plt.text(eval(para[0]),eval(para[1]),a,color='white',fontsize=5)

#save image
plt.savefig('bonding-elements.png',dpi=600)
#crop image
image=Image.open('bonding-elements.png')
box = (858, 343, 3080, 1580)
cropped_image = image.crop(box)
#save cropped image
cropped_image.save('bonding-elements.png')

image = Image.open('bonding-elements.png')
image = image.convert("RGB")
result_image = Image.new("RGB", image.size, "white") 

for x in range(image.width):
    for y in range(image.height):
        r, g, b = image.getpixel((x, y))
        if not (r == 0 and g == 0 and b == 0):  
            result_image.putpixel((x, y), (r, g, b))
 

result_image.save('bonding-elements.png')
#result_image.show()
image=Image.open('bonding-elements.png')
box = (5, 9, 2215, 1225)
cropped_image = image.crop(box)
#save cropped image
cropped_image.save('bonding-elements.png')
