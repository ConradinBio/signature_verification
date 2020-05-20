# Signature Verification

## Feature selection and scaling
Here we can see two features of a signature, the x and y position of the pen at a given time point (the time dimension is flattened in the plot). We can see the effect of `RobustScaler` by the `sklearn` library. 

![](./report_figures/non_normalized.png)
![](./report_figures/normalized.png)

Adding a third feature, `pressure` we can see the necessity; pressure has a much wider range (0-1000) than the two position features (0-35), and would dominate any function calculating the distance between two signatures, dwarfing any distances calculated on the two positional features. This time using `MinMaxScaler`, which is less robust to outliers, but allows us to restrict the output to a fixed range of values (0-1).
![](./report_figures/min_max_scaler.png)

When fitting the normalization function to each signature individually, we loose the absolute differences between two signatures. Example: Person A pressed the pen consistently but really hard when signing, person B impersonating person A also presses the pen consistently but softer - we cannot differentiate these two if we normalize them individually, even tough this would be a good discriminator. Instead we need to fit the scaler to the whole train set, and only then apply to each individual signature. When testing, we need to use the scaler fitted on the training data to normalize it. In other other words: If we normalize and fit the scaler to each signature individually, we only keep the realtive differences inside the signatures, and loose the absolute differences between the signatures.

As features we selected:
```
[:,0] =  position x
[:,1] =  position y
[:,2] =  speed v(x)
[:,3] =  speed v(y) 
[:,4] =  pressure
```
## Dynamic Time Warping
The distances for each signature between the enrollment set and the validation set was calculated. Because each signature has different feature lengths, their distances can not be compared across different signatures. Therefore we normalized the distances by dividing each distance by the mean-distance wthin the enrollment. Only the minimal distance for each signature from the verification set to the enrollment set was kept.
