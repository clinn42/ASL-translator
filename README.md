## ASL Alphabet translator

---

A Python application that is can detect the hand sign for American Sign Language alphabets and can be used to string together sentences.

[ASL Alphabet Dataset](https://www.kaggle.com/grassknoted/asl-alphabet)

#### Details:

- ASL dataset by grassknoted on [kaggle](www.kaggle.com)
- **Size** : 1GB
- Consits of 29 Hand signs for letter A -Z, space, delete and blank
- There are 3000 images for each symbol in different orientations and lighting.
- Total dataset size = 3000 images x 29 catergories x 12kb per image = 1GB

### Required python packages:

- Keras
- Tkinter
- Numpy
- OpenCV
- Pillow

It makes use of the Convolutinal Neural Networks to train a model to identify the image/hand signature made in the detection area.

- Model classifies the image into one of 29 classes, alphabets A - Z, space, delete and blank.
- It was constructed and trained utilizing Kaggle's GPU.
- **Model**: kagg_aslmod2_gray.h5
- Model trained on Grayscale images

### Main program: main.py
