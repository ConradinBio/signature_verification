# Final Report: Pattern recognition

## Group organization
As most of us were unfamiliar with github we first had to get used to it. Once everything was set up we met via conference call several times to discuss the projects and to assign individual tasks. We also tried to exchange regularly and to clarify ambiguities.
For the first group project (MNIST) we assigned people to each subtask which went very good as we then had a maximum of two people working on a single task and allowed us to work closely together and remove obscurities early on.
The second group project was larger. We therefore split the task into subtasks. The consequence of this was that everyone had a very narrow focus on a specific task, which turned out to be too narrow - we had trouble keeping an eye on the big picture until the last couple of zoom-meetings. At this point we had already ran out of time to make major adjustments, which would be necessary to improve our results.
For the third and last group project we started earlier and assigned some tasks twice which was a good idea. we had enough time to finalize our project. 

---TODO---- (delete later)
For each task (MNIST, Keyword Spotting, 3rd group exercise)
  What is special about your solution
  What was your approach
  What worked, what did not work
---- ----- ---

## Exercise 1: MNIST
Link to repository and report: [pattern_recognition](https://github.com/hinderling/pattern_recognition)

### SVM
For this task we used sklearn which provides the svm model. We were supposed to implement one model with a linear kernel and one with an RBF (Radial Basis Function) kernel. The optimal parameters of C and in the RBF case also gamma were estimated using grid search (also provided by sklearn).

### MLP
The Multi-layer Perceptron was implemented using the SciKit Library, which also offers nice (visual) comparisons and explenations of different classifiers, which really helped us to get going.
Special about our solution for the multilayer perceptron was that we did extensive parameter testing by applying a gridsearch. For different parameter combinations we visualized the weights of the hidden neurons, to understand why a particular set of parameters does or does not work well. Visualization helped us a lot to find better parameters - be it in displaying the results of the gridsearch in a heatmap or visualizing the neurons. The shuffling experiments helped us to understand the real-world case of overfitting. Writing an extensive report helped to really understand the functioning of an MLP, and not just apply it.

### CNN
A CNN was applied to the full MNIST dataset and the the permutated MNIST dataset.
Our approach for the CNN implementation was that we first found a [nice tutorial](https://deeplizard.com/learn/video/MasG7tZj-hw) about neural network programming which we both went through in order to understand what we had to do. After that we discussed our notes and went on implementing our CNN together.
what worked, what did not work: We were not able to implement CUDA to make use of the GPU for tensor calculations, this would speed up the calculations quite a bit. Therefore runtime was one problem as we had to run our CNN over night. At that time we were not used to github so we exchanged pieces of codes manually which was a big hustle but worked as we were only two working on that task.

## Exercise 2: Keyword spotting
Link to repository and report: [keyword_spotting](https://github.com/hinderling/keyword_spotting)

#### Special thing
#### Approach
Again the SciKit Library documentation and [examples](https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html) helped us - this time when deciding on a scaler, that we could use to do the data normalization. Visualizing the data pre and post scaling helped us to understand how the data stays the same relatively, and just the axis change - when stretching the scaled x and y pen-position data into the same window as the unstretched data, the two signatures look the same.
#### What worked
We were able to calculate distances using dtw and also draw recall/precision curves. 
#### What not worked
We did not normalize the features and we calculated a separate recall/precision curve for every feature. This is because we were not aware that the dtw function takes multiple feature vectors as argument. Of course, considering all features together would yield a much better result. 

## Exercise 3: Signature verification
#### Special thing
#### Approach
The aim of this project was to tell whether a signature is an original or a forgery based on five features and an enrollment set of 5 original signatures per user. Distances were calculated using fastdtw. First, we calculated the mean distance & its standard deviation among each of the users five original signatures. Then, we calculated the distance between each validation set signature and the corresponding five signatures in the enrollment set; only the minimal distance was kept. This distance was then normalized (xi-mean/std) and ordered from lowest to largest. 
For the evaluation, we iteratively added the image with the lowest distance to the 'hits' and recalculated the recall and precision value. From this, we then drew the recall/precision curve. 
#### What worked
This time, we normalized the features and we calculated a recall/precision curve considering all features together. This exercise helped us a lot to clarify the issues we had before, for the Keyword spotting. 
#### What not worked
The max distance in std obtained to achieve the max precision was neg. This means that there is one very good forgery in the validation dataset, that varies less from the 5 enrollment originals than those originals vary among each other. Including more features could potentially solve this issue. 

## General thoughts/feedback about group exercise
We think that it is very important to have such group exercises, particularly because it forces us to get used to github, which is most valuable for the future. Also, in the 2 exercise, we learned that it is very important to be aware of the big picture, even if everyone is responsible for a small subtask. Generally, group tasks can be a big chance to get a broader view, as the ideas of everyone can be discussed. 
