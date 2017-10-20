#Python Program to read in bites and print them into console and save them as images
#Created by : Robert Kiliszewski	
#Date: 15/10/2017

#Imports (PIL is for Pillow in order to save images)
import gzip
import PIL.Image as pilImage
import numpy as np

#Read labels from file
def read_labels_from_file(filename):
    with gzip.open(filename, 'rb') as f:
        magic = f.read(4)
        magic = int.from_bytes(magic, 'big')
		
        print("Magic is: ", magic)
		
        nolab = f.read(4)
        nolab = int.from_bytes(nolab, 'big')
		
        print("Number of labels: ", nolab)
		
        labels = [f.read(1) for i in range(nolab)]
        labels = [int.from_bytes(label, 'big') for label in labels]

        return labels

#Read images from file
def read_images_from_file(filename):
    with gzip.open(filename, 'rb') as f:
        magic = f.read(4)
        magic = int.from_bytes(magic, 'big')
		
        print("Magic is: ", magic)
		
        noimages = f.read(4)
        noimages = int.from_bytes(noimages, 'big')
		
        print("Number of images: ", noimages)
		
        norows = f.read(4)
        norows = int.from_bytes(norows, 'big')
		
        print("Rows: ", norows)
		
        nocols = f.read(4)
        nocols = int.from_bytes(nocols, 'big')
		
        print("Columns: ", nocols)

		#Create empty array called images
        images = []

		#Run through the images
        for i in range(noimages):
            rows = []
            for r in range(norows):
                cols = []
                for c in range(nocols):
					#Append Bytes into arrays
                    cols.append(int.from_bytes(f.read(1), 'big'))
                rows.append(cols)
            images.append(rows)

        return images
		
#This Prints the image to the console	
def print_image(image):
    for row in image:
        for col in row:
            print(' . ' if col < 128 else ' # ', end=' ')
        print()
		
#Image save function
def save_image(image, tag, index, label):
    target = "images/%s-%05d-%d.png"
    
    pixels = np.array(image)
    img = pilImage.fromarray(pixels.astype('uint8'))
    img.save(target % (tag, index, label))

#Read Labels
train_labels = read_labels_from_file('data/train-labels-idx1-ubyte.gz')
test_labels = read_labels_from_file('data/t10k-labels-idx1-ubyte.gz')

#Read Images
train_images = read_images_from_file('data/train-images-idx3-ubyte.gz')
test_images = read_images_from_file('data/t10k-images-idx3-ubyte.gz')

#print image of X index
print_image(train_images[4999])

for i in range(len(train_images)):
    save_image(train_images[i], 'train', (i+1), train_labels[i])

for i in range(len(test_images)):
    save_image(test_images[i], 'test', (i+1), test_labels[i])