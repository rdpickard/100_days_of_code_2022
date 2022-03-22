# Dog detector with CNN

---
```
Language: Python
Brief: A convolutional neural network based dog in image detctor    
Scope:  
Tags: ai, computer vision
State: 
Result: 
```
---

I post pictures of my dog a lot. I am going to make a twitter bot that watches my posts and when it detects a dog picture, it will reply with some encouragement like "Give lily a treat!". 

I am hoping to benefit from her cuteness so she should get rewarded. 

Using a CNN for dog detection seems like a good start.



### Results

---

### If I was to do more

---

### Notes

- dog data set https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/dogImages.zip
- scitkit-learn https://scikit-learn.org/stable/
- Keras https://keras.io/
- To install tensorflow had to use `pip install tensorflow-macos`. 
  - Had to find this through google. not on tensor flow main pages. Other wise get an error 
    - ```ERROR: Could not find a version that satisfies the requirement tensorflow (from versions: none) ERROR: No matching distribution found for tensorflow```
  - had to install 'pkg-config' with homebrew. Otherwise pip installing tensorflow gets an error
    - `Building h5py requires pkg-config unless the HDF5 path is explicitly specified`
  - had to install hdf5 with homebrew and set the environment var `export HDF5_DIR=$(brew --cellar hdf5)/1.13.0`  Otherwise pip installing tensorflow gets an error
    - `error: Unable to load dependency HDF5, make sure HDF5 is installed properly`
- Using requirements.txt file seperate from main one. Getting the ML packages installed was a pain in the ass 

---

### Example 

---