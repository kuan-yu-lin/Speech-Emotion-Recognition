# Speech_Emotion_Recognition

###### University Stuttgart
###### Introduction to Deep Learning for Language and Speech Processing Project, Winter 2022/23

## Project Information

### Description

Predict the emotion class given the features of a speech input. There are 4 classes, where we use a two-dimensional representation: 

             |VALENCE = 0|VALENCE = 1
  AROUSAL = 1|   anger   |    Joy    
  AROUSAL = 0|  sadness  |  Pleasure 

### Requirements

The code should run the enviroment as follow list:
  name|version
  :---:|:---:
  python|3.10.8
  pandas|1.5.3
  numpy|1.24.2
  tensorflow|2.11.0
  scikit_learn|1.2.1

### Results

Model Accuracy: 50.38%
Accuracy of Development Dataset: 49.94% 
(The highest score in class: 53.29%)

## Dataset

Please email st180665@stud.uni-stuttgart.de to get the dataset.

## Run

Before running the code, you sholud set up the enviroment we needed by entering the following command into the terminal: 
  * `pip install -r requirement.txt`  
  
and then verify the parameter of dataset path in __main.py__  
  * `__train_file_path__ = 'your_dataset_path'`
  * `__dev_file_path__ = 'your_dataset_path'`

```
    python3 main.py
```


