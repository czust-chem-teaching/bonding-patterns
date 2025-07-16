import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import string
import networkx as nx
from PIL import Image
from matplotlib.colors import ListedColormap
 

parser = argparse.ArgumentParser()
parser.add_argument("name1", type=str)
args = parser.parse_args()
G = nx.read_edgelist('data.txt', create_using=nx.Graph())#undirected graph to delete the duplicated data
temp=[]
print('is processing ...',args.name1)
#get bonding elements of args.name1
for k in G.neighbors(args.name1):
   temp.append(k)
#define your own colow map here:
colors = ['green', 'blue', 'orange', 'black','white']

cmap = ListedColormap(colors)
#draw the grid similar to the Periodic Table
grid = np.zeros([18, 18])

grid[0:1, 1:17] = 4
grid[1:3, 2:12] = 4
grid[10:18,0:18] = 4 
grid[5:9,2:3] =4# blank for lanthanoid and actinide 
grid[7:8,0:18] =4
grid[8:10,0:3]=4
#legend
grid[1:2, 6:7] = 2
grid[1:2, 7:8] = 1
grid[1:2, 8:9] = 0
# fill bonding elements with blue 
with open("location.txt","r") as filestream2:
  for line2 in filestream2:
    line3 = line2.strip('\n') 
    loc   = line3.split(",")
    if loc[0] in temp:
       grid[eval(loc[1]):eval(loc[2]),eval(loc[3]):eval(loc[4])]=1
with open("location.txt","r") as filestream3:
   for line4 in filestream3:
     line5 = line4.strip('\n')
     loc   = line5.split(",")
     if loc[0] == args.name1:
        grid[eval(loc[1]):eval(loc[2]),eval(loc[3]):eval(loc[4])]=2
#set the color scheme
plt.imshow(grid, cmap=cmap, interpolation='nearest')
#set the style of grid
plt.grid(True, which='both', color='white', linewidth=0.07)
#draw X and Y lables
plt.xticks(np.arange(-0.5, 18, 1),(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"]),fontsize=8)
plt.yticks(np.arange(-0.5, 18, 1),(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19"]),fontsize=8)
#draw element name in each grid
with open("text.txt","r") as filestream1:
  for line in filestream1:
    line1= line.strip('\n') 
    para=line1.split(",")
    plt.text(eval(para[0]),eval(para[1]),para[2],color='white',fontsize=7)
plt.text(5.85,1.2,'E',color='white',fontsize=7,fontweight='bold')
plt.text(6.7,1.2,'BE',color='white',fontsize=6,fontweight='bold')
plt.text(7.55,1.2,'NBE',color='white',fontsize=6,fontweight='bold')


polygon_x = [1.53, 2.46, 2.46, 1.53]  
polygon_y = [4.69, 7.52, 8.31, 5.47]  
plt.fill(polygon_x, polygon_y, color='cyan',closed='True')
polygon_x = [1.53, 2.47, 2.48, 1.53]  
polygon_y = [5.69, 8.52, 9.31, 6.47]  
plt.fill(polygon_x, polygon_y,color='cyan',closed='True')
line_x = [1.51,2.5]
line_y = [5.49,8.52]
plt.plot(line_x, line_y, color='white', linestyle='-', linewidth=0.3)
#save image
plt.savefig(args.name1+'.png',dpi=600)
#crop image
image=Image.open(args.name1+'.png')
box = (858, 343, 3080, 1580)
cropped_image = image.crop(box)
#save cropped image
cropped_image.save(args.name1+'.png')
image = Image.open(args.name1+'.png')
 

image = image.convert("RGB")
 

result_image = Image.new("RGB", image.size, "white") 

for x in range(image.width):
    for y in range(image.height):
        r, g, b = image.getpixel((x, y))
        if not (r == 0 and g == 0 and b == 0):  
            result_image.putpixel((x, y), (r, g, b))
 

result_image.save(args.name1+'.png')
#result_image.show()
image=Image.open(args.name1+'.png')
box = (5, 9, 2215, 1225)
cropped_image = image.crop(box)
#save cropped image
cropped_image.save(args.name1+'.png')
