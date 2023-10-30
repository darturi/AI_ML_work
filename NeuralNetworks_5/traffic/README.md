My first moment of true experimentation/exploration over the course of this 
project came when I was having a great deal of trouble with the load data 
function. Things were not outputting correctly and I was confused as to why. 
So I added an abundance of print statements for the numpy arrays and 
discovered that by using the resize function from numpy I was actually 
cropping the image to the upper left hand corner rather than truly resizing
 it. So I took to the cv2 documentation and discovered an alternate resize 
 method that could preserve the image with the number of pixels I was looking 
 for. However, my experimentation certainly did not end there.

I started off the construction of my neural net as modeled directly after the 
source code from lecture. Obviously this model did not function for the data 
in this different problem, so the first change I made was to alter the input 
and output shapes to account for the data in this problem. That meant changing
input sizes to (30, 30, 3) using the IMG_WIDTH and IMG_HEIGHT variables, and 
changing the size of the output layer to 43 using the NUM_CATEGORIES variable.
In the source code I was starting from there was a single hidden layer with 
128 units, but after running this initial version of the model I was greeting 
with dismal results. There was a dropout of 0.5 after the hidden layer, 32 
filters at a 3x3 kernel, and a max pooling layer (2x2). 

Hidden layer experimentation: 
In section we learned that a neural net can solve pretty much anything given 
enough hidden layers and enough units, so I began to experiment with adding 
hidden layers. As I started at 128 I was simply copy and pasting that line of 
code. After trying two then three hidden layers I was disappointed at how long
the code was taking to run, so I reduced the size of the hidden layers to 50 
across all three. Not only did the time improve, but so did accuracy. In this 
moment of experimentation I learned that there is not a purely positive 
relationship between the size of hidden layers and the accuracy of a model. 
As I added more and more hidden layers, I learned that there was a similar 
point of diminishing returns for the number of layers as well as the number 
of units contained within each. I found those points by sheer trial and error,
lots of tests, and homing on slowly on what worked and what did not. 

Hidden Layer Trial and Error:
1 hidden layer, units: [128]
2 hidden layers, units: [50, 50]
2 hidden layers, units: [160, 50]
3 hidden layers, units: [50, 50, 50] 
4 hidden layers, units: [50, 50, 50, 50]
5 hidden layers, units: [50, 50, 50, 50, 50] 
6 hidden layers, units: [50, 50, 50, 50, 50, 50]
5 hidden layers, units: [50, 50, 50, 50, 50] 
5 hidden layers, units: [60, 60, 60, 60, 60]
5 hidden layers, units: [70, 70, 70, 70, 70]
5 hidden layers, units: [65, 65, 65, 65, 65]
5 hidden layers, units: [80, 80, 80, 80, 80]
5 hidden layers, units: [75, 75, 75, 75, 75]
5 hidden layers, units: [75, 70, 65, 60, 55] 
5 hidden layers, units: [75, 75, 65, 65, 55]
5 hidden layers, units: [80, 80, 80, 80, 80]
5 hidden layers, units: [90, 90, 90, 90, 90]
5 hidden layers, units: [80, 70, 70, 70, 70]
4 hidden layers, units: [80, 70, 70, 70]

Note: the above adjustments listed are within the context of other kinds of 
adjustments interspersed between adjustments to the number and size of hidden 
layers.

Note: I only adjusted dropout when I noticed that the accuracy of the previous
epochs was greater than that of the final analysis. By repeating this process,
and tweaking little by little when changes were necessary I ended up with a 
dropout of 0.6 after the last hidden layer. 

Besides hidden layers the next thing I began to experiment with were 
activation functions. In my experimentation I grouped activation layers into 
three distinct categories based on where in the model definition they were 
applied: before flattening units, within the hidden layers, and in the output
layer. The first obstacle I faced was the simple fact that besides a very 
limited set, I was not aware of the options available for use in activation 
function. So I navigated to the documentation for activation functions and 
begin looking through them, trying some out before understanding the math 
behind them, just having looked at the graph and experimenting through trial 
and error. First I replaced the ReLu activation function in the hidden layers 
with the sigmoid activation function to drastically worse accuracy, cementing 
the importance of this function. I followed this with softmax to equally 
terrible results. However, this pattern reversed as I tried SeLu with 
heightened accuracy. So, at SeLu it stayed. I repeated this step with the 
filter and pooling layers to come to the same conclusion. The output layer 
activation function was left unchanged. (From softmax)

The final element of this project that I experimented with were the 
filter and pooling layers. To solve for the best solution I could come up 
with, with limited knowledge of the true mathematics behind the filters I 
was applying (besides the general things taught in lecture)., I decided to 
pursue a similarly trial and error based approach as taken with the hidden 
layers. I kept all the pooling layers at a consistent size as to not lose too 
much of the image, but ended up discovering that a certain gradient of filter 
sizes generated better results with less parameters that consistently sized, 
large filers at every turn. These filter sizes were what I noticed as having 
the greatest impact on runtime for the program, purely in my personal 
experience, so I tried to keep them at a minimum. After experimentation with 
1 through 5 pairs of filter / pooling layers I ended up with 4 filter layers 
and 3 pooling layers. 

The last element that I added were batch normalization layers. These were not 
something that I was initially familiar with, but I ended up adding them 
anyways. I had hit a ceiling of about 89% accuracy by tinkering with the above
described elements of my model and I was becoming increasingly frustrated, 
so I turned to the internet for research. Through a dive through google I 
found mentions of something called batch normalization. So, I went to the 
tensorflow documentation and read up on it and it sounded very desirable, 
promising quicker training for my model. I added it in after my hidden layers
 and was pleasantly surprised to find my accuracy increased. I was even more 
 happily surprised to find that the improvement could be extended it batch 
 normalization was applied after every hidden layer and every filter pooling 
 pair. Using batch normalization I was able to consistently crack 94% 
 accuracy, even if it took a little bit longer for the program to run.

Note: These experiments were not done in the order in which they were 
written about, they were written this way for the sake of clarity. 