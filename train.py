# -*- coding: utf-8 -*-

import numpy as np
np.random.seed(1)
from matplotlib import pyplot as plt
import skimage.data
from skimage.color import rgb2gray
from skimage.filters import threshold_mean
from skimage.transform import resize
import network
import cv
import os


# Utils
def get_corrupted_input(input, corruption_level):
    corrupted = np.copy(input)
    inv = np.random.binomial(n=1, p=corruption_level, size=len(input))
    for i, v in enumerate(input):
        if inv[i]:
            corrupted[i] = -1 * v
    return corrupted

def reshape(data):
    dim = int(np.sqrt(len(data)))
    data = np.reshape(data, (dim, dim))
    return data

def plot(data, test, predicted, figsize=(5, 6)):
    data = [reshape(d) for d in data]
    test = [reshape(d) for d in test]
    predicted = [reshape(d) for d in predicted]

    fig, axarr = plt.subplots(len(data), 3, figsize=figsize)
    for i in range(len(data)):
        if i==0:
            axarr[i, 0].set_title('Train data')
            axarr[i, 1].set_title("Input data")
            axarr[i, 2].set_title('Output data')

        axarr[i, 0].imshow(data[i])
        axarr[i, 0].axis('off')
        axarr[i, 1].imshow(test[i])
        axarr[i, 1].axis('off')
        axarr[i, 2].imshow(predicted[i])
        axarr[i, 2].axis('off')

    plt.tight_layout()
    plt.savefig("result.png")
    plt.show()

def preprocessing(img, w=128, h=128):
    # Resize image
    img = resize(img, (w,h), mode='reflect')

    # Thresholding
    thresh = threshold_mean(img)
    binary = img > thresh
    shift = 2*(binary*1)-1 # Boolian to int

    # Reshape
    flatten = np.reshape(shift, (w*h))
    return flatten

def main():
    # Load data
    #camera = skimage.data.camera()
    data = []

    input_images_train_path = '/home/iron/tp2ia/Hopfield-Network/imgs/fotos_entrenar/hirigama/'    
    files_names = os.listdir(input_images_train_path)

    #print(files_names)

    for file in files_names:
        data.append(rgb2gray(skimage.io.imread(input_images_train_path + file)))

    


    #prueba = rgb2gray(skimage.io.imread("/home/iron/tp2ia/Hopfield-Network/imgs/fotos_entrenar/hirigama/N.jpg"))
    #astronaut = rgb2gray(skimage.data.astronaut())
    #horse = skimage.data.horse()
    #coffee = rgb2gray(skimage.data.coffee())
    

    #prueba1 = rgb2gray(skimage.io.imread("/home/iron/tp2ia/Hopfield-Network/imgs/fotos_entrenar/hirigama/KE.jpg"))
    #prueba2 = rgb2gray(skimage.io.imread("/home/iron/tp2ia/Hopfield-Network/imgs/fotos_entrenar/hirigama/MO.jpg"))
    #prueba3 = rgb2gray(skimage.io.imread("/home/iron/tp2ia/Hopfield-Network/imgs/fotos_entrenar/hirigama/SHI.jpg"))#
    #prueba4 = rgb2gray(skimage.io.imread("/home/iron/tp2ia/Hopfield-Network/imgs/fotos_entrenar/hirigama/MO.jpg"))
    
    
    #prueba5 = rgb2gray(skimage.data.astronaut())
    #prueba6 = rgb2gray(skimage.data.coffee())

    
    # Marge data
    #data.append(astronaut)
    #data.append(horse)
    #data.append(coffee)

    # Preprocessing
    print("Start to data preprocessing...")
    data = [preprocessing(d) for d in data]

    # Create Hopfield Network Model
    model = network.HopfieldNetwork()
    model.train_weights(data)

    # Generate testset
    test = [get_corrupted_input(d, 0.3) for d in data]

    predicted = model.predict(test, threshold=0, asyn=False)
    print("Show prediction results...")
    plot(data, test, predicted)
    print("Show network weights matrix...")
    #model.plot_weights()

if __name__ == '__main__':
    main()
