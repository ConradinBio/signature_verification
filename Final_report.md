# Final Report

## Group organization
As most of us were unfamiliar with github we first had to get used to it. Once everything was set up we met via conference call several times to discuss the projects and to assign individual tasks. We also tried to exchange regularly and to clarify ambiguities.
For the first group project (MNIST) we assigned people to each subtask which went very good as we then had a maximum of two people working on a single task and allowed us to work closely together and remove obscurities early on.
The second group project was larger. We therefore split the task into subtasks. The consequence of this was that everyone had a very narrow focus on a specific task, which turned out to be too narrow - we had trouble keeping an eye on the big picture until the last couple of zoom-meetings. At this point we had already ran out of time to make major adjustments, which would be necessary to improve our results.
For the third and last group project we started earlier and assigned some tasks twice which was a good idea. we had enough time to finalize our project. 

For each task (MNIST, Keyword Spotting, 3rd group exercise)
  What is special about your solution
  What was your approach
  What worked, what did not work

## MNIST 
### CNN
A CNN was applied to the full MNIST dataset and the the permutated MNIST dataset.
Our approach for the CNN implementation was that we first found a nice tutorial about neural network programming which we both went through in order to understand what we had to do (https://deeplizard.com/learn/video/MasG7tZj-hw). After that we discussed our notes and went on implementing our CNN together.
what worked, what did not work: We were not able to implement CUDA to make use of the GPU for tensor calculations, this would speed up the calculations quite a bit. Therefore runtime was one problem as we had to run our CNN over night. At that time we were not used to github so we exchanged pieces of codes manually which was a big hustle but worked as we were only two working on that task.

## Keyword spotting
#### Special thing
#### Approach
#### What worked
#### What not worked
We did not normalize the features and we calculated a separate recall/precision curve for every feature. This is because we were not aware that the dtw function takes multiple feature vectors as argument. 

## Signature verification
#### Special thing
Write something about this maxmin normalizer, Lucien/Cuba?:)
#### Approach
The aim of this project was to tell whether a signature is an original or a forgery based on five features and an enrollment set of 5 original signatures per user. Distances were calculated using fastdtw. First, we calculated the mean distance & its standard deviation among each of the users five original signatures. Then, we calculated the distance between each validation set signature and the corresponding five signatures in the enrollment set; only the minimal distance was kept. This distance was then normalized (xi-mean/std) and ordered from lowest to largest. 
For the evaluation, we iteratively added the image with the lowest distance to the 'hits' and recalculated the recall and precision value. From this, we then drew the recall/precision curve. 
#### What worked
#### What not worked
The max distance in std obtained to achieve the max precision was neg. This means that there is one very good forgery in the validation dataset, that varies less from the 5 enrollment originals than those originals vary among each other. Including more features could potentially solve this issue. 

## General thoughts/feedback about group exercise
