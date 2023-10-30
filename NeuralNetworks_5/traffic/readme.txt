One hidden layer with 128
2 hidden layers with 50
2 hidden layers one with 160 one with 50 (loss: 3.4907 - accuracy: 0.0548)
Remove the dropout from the first hidden layer (loss: 3.4930 - accuracy: 0.0573)
Up from 32 filters applied to 64 (loss: 3.4968 - accuracy: 0.0574) (took longer)
Filters back down to 32 and now with three hidden layers each w 50 nodes (one dropout at end of 0.5) (loss: 1.4259 - accuracy: 0.4753)
Same as before plus one hidden layer w 50 nodes (loss: 0.7505 - accuracy: 0.7691)
Added a max pooling layer after the second hidden layer (failed)
Added a fifth hidden layer with 50 units (loss: 0.3985 - accuracy: 0.8893)
Added a sixth hidden layer with 50 units (loss: 0.5839 - accuracy: 0.8314)
Remove sixth hidden layer (loss: 0.5023 - accuracy: 0.8581)
# Note that at some point along the way a sixth hidden layer was added
Replace ReLu activation func in hidden layers with sigmoid (loss: 3.5007 - accuracy: 0.0496)
return all to ReLu (loss: 1.3769 - accuracy: 0.5175) (loss: 1.4727 - accuracy: 0.4674)
Add dropout 0.5 after third hidden layer (loss: 1.5316 - accuracy: 0.4353)
remove 2nd dropout layer and change activation to softmax on hidden layers (loss: 3.4964 - accuracy: 0.0538)
remove 6th hidden layer (loss: 3.4950 - accuracy: 0.0569)
return all to relu (loss: 1.0242 - accuracy: 0.6348)
increase units in all hidden layers to 60 (loss: 0.3777 - accuracy: 0.9014)
increase units in all hidden layers to 70 (loss: 0.3805 - accuracy: 0.9106)
increase units in all hidden layers to 65 (loss: 0.6440 - accuracy: 0.7923) (loss: 0.4623 - accuracy: 0.8768)
increase units in all hidden layers to 80 (loss: 0.4676 - accuracy: 0.8980) (Note: past 4 epochs had better scores)
Up dropout to 0.6 (loss: 0.4873 - accuracy: 0.8736) Previous were worse  (loss: 0.3923 - accuracy: 0.8911) Previous were worse
increase units in all hidden layers to 75 (loss: 0.5485 - accuracy: 0.8466) (loss: 3.5030 - accuracy: 0.0563)(loss: 0.4025 - accuracy: 0.89250) (loss: 0.6715 - accuracy: 0.8213)
Add     """
        tf.keras.layers.Conv2D(15, activation='selu', kernel_size=3, padding="same"),
        tf.keras.layers.MaxPool2D(pool_size=2),
        tf.keras.layers.Conv2D(10, activation='selu', kernel_size=3, padding="same"),
        tf.keras.layers.MaxPool2D(pool_size=2),
        tf.keras.layers.Conv2D(5, activation='selu', kernel_size=3, padding="same"),
        tf.keras.layers.MaxPool2D(pool_size=2),
        tf.keras.layers.Conv2D(5, activation='selu', kernel_size=3, padding="same"),
        """
        Before flatten (loss: 1.6237 - accuracy: 0.4438)
Remove last two lines from recently added block (loss: 0.7933 - accuracy: 0.7355) (loss: 0.7961 - accuracy: 0.7343)
turn pooling from newly added pooling layers from 2 to (2,2) (loss: 0.7105 - accuracy: 0.7420)
change hidden layers from [75, 75, 75, 75, 75] to [75, 70, 65, 60, 55] (loss: 0.7138 - accuracy: 0.7733) (loss: 0.7052 - accuracy: 0.7625) (loss: 1.1673 - accuracy: 0.5912)
change relu activation function to selu (loss: 0.5303 - accuracy: 0.8321)
change hidden layers from [75, 70, 65, 60, 55] to [75, 75, 65, 65, 55] (loss: 0.4280 - accuracy: 0.8652) (loss: 0.4614 - accuracy: 0.8544) (loss: 0.4575 - accuracy: 0.8551)
change hidden layers from [75, 75, 65, 65, 55] to [80, 80, 80, 80, 80] (loss: 0.3625 - accuracy: 0.8925) (loss: 0.3895 - accuracy: 0.8766) (loss: 0.3646 - accuracy: 0.8917)
change hidden layers from [80, 80, 80, 80, 80] to [90, 90, 90, 90, 90] (loss: 0.3911 - accuracy: 0.8799) (loss: 0.4672 - accuracy: 0.8514) (loss: 0.4648 - accuracy: 0.8560)
change hidden layers to [80, 70, 70, 70, 70] (loss: 0.6751 - accuracy: 0.7864) (loss: 0.3953 - accuracy: 0.8803) (loss: 0.3809 - accuracy: 0.8840)
Add batch normalization after 2nd and 4th hidden layers (loss: 0.3337 - accuracy: 0.8970)
Add batch normalization after every hidden layer (loss: 0.3828 - accuracy: 0.8745) (loss: 0.3370 - accuracy: 0.8963)
change to relu (loss: 0.8043 - accuracy: 0.7428)
Undo and cut one hidden layer (loss: 0.2623 - accuracy: 0.9215) (loss: 0.4563 - accuracy: 0.8521) (loss: 0.2855 - accuracy: 0.9155) (loss: 0.2603 - accuracy: 0.9161)
Add dropout 0.5 after every hidden layer (loss: 0.8354 - accuracy: 0.7309) (loss: 0.9952 - accuracy: 0.6330)
revert to line 46 state (loss: 0.2725 - accuracy: 0.9196)
Add batch normalization after each two layers of the filtering and pooling step (loss: 0.1564 - accuracy: 0.9520) (loss: 0.1861 - accuracy: 0.9431) (loss: 0.1328 - accuracy: 0.9602) (loss: 0.1474 - accuracy: 0.9562)
padding = 'valid' does not work Crashes program

