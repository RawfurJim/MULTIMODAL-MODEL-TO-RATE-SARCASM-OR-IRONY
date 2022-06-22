# MULTIMODAL-MODEL-TO-RATE-SARCASM-OR-IRONY

# Main Work
The main aim of this project is to detect and rate Sarcasm/Irony with Multimodal (where there is image with comment) data.
For this project we have used dataset of a Facebook Group. In this dataset the snapshot of memes/picture with top 1-3 comments (Italian) were given. 
The ranking was done based on Likes. We have built three models.  We used unimodal BERT only on the comments as well as Multimodal,
where ResNet for image BERT for text and Fusion to join both models. We also another Multimodal where ResNet for image and Fasttext for text analysis and
then used fusion to join both models. Our main target of this project was to detect whether comment will get 500 Likes or not and which approach is giving best result is it unimodal or Multimodal. 

# Data

Our main Data Source is from a Italian community Facebook group. In this group the admin would post funny image/ memes and the group member would post funny comments in these memes.Then top the winner would be selected in the bases of top Likes. 
They gave the screenshot of the memes with the most funny comments to Ficcadenti Valerio. He then modified the screenshot and made two separate file one with images and another csv file with image_name, comments and Likes. 
In our project we try to build a model where we can predict if the comments will get more then 500 Likes or not.

<img width="319" alt="excel" src="https://user-images.githubusercontent.com/64610564/175053192-74138eed-a164-4a10-a8cf-31af65fa2763.PNG">

# Models

Our first building model was a multimodal model where we have used Fasttext (Joulin, et al., 2016) for text and ResNet (He, et al., 2016) for image. All of the model building was done by framework Pytorch. There are many library available in Pytorch like torch and Pytorch Lighting. 
To build this model we have used baseline code Multimodal Modal which was first developed by DrivenData (Fitzpatrick, 2020) a company who partnered with 
Facebook for it’s Hateful Memes Challenge competition. 

# Fasttext with ResNet

   Our main modal have been build with the base of three main classes “HatefulMemesDataset”, “LanguageAndVisionConcat” and “HatefulMemesModel”. 
   These classes have unique work function. First, lets talk about the “HatefulMemesDataset” class. This class is responsible for loading the data from different
   modalities and transform the data. It takes the image and text dataset one by one. Transform the image with torchVision and text for Fasttext and return a tensor.
   At the end this class will return a dictionary with keys for each  id, text, image and label.
   
   <img width="422" alt="fasttext" src="https://user-images.githubusercontent.com/64610564/175057692-66840c60-9e23-461f-99e1-2bbfc87641b5.PNG">
   
   We'll run our image information mode through a image model and result the last arrangement of element portrayals in our "LanguageAndVisionConcat" architecture, then do likewise for our language mode. Then we'll link these feature representations into another component vector, which we'll go through a fully connected layer for classification.
   The language and vision modules will be utilized as parameters in our mid-level fusion model.
   
   <img width="368" alt="multimodal_modal" src="https://user-images.githubusercontent.com/64610564/175058085-f8c737b1-780b-42ab-a912-f3a74342c30a.PNG">
   
   To prepare our Modal, we'll utilize PyTorch Lightning. We get the vast majority of the training logic "free of charge" in the background by subclassing the PyTorch Lightning LightningModule. We just have to indicate what a forward call and preparing step are, as well as deal a train dataloader to our model. Checkpoint saving and early halting can be parameterized, but they aren't required because Lightning takes care of the intricacies (Fitzpatrick, 2020).We'll create a HatefulMemesModel LightningModule subclass that accepts a Python dictionary of hyperparameters called hparams that may be used to tailor the instantiation.
   When we generate a submission to the competition, this pattern is a Lightning convention that allows us to simply import learned models for future use.
   
# Bert with RenNet

   Our second building model was a multimodal model where we have used Bert  for text analysis and ResNet  for 
   image analysis. All of the model building was done by framework Pytorch. We have used the same baseline code Multimodal Modal which was first 
   developed by DrivenData a company who partnered with Facebook for it’s Hateful Memes Challenge competition. 
   In our second implementation, the main difference is for text analysis we have used Bert rather than Fasttext.
   However, to implement Bert we had to face some challenge  like, as my whole modal was built with Pytorch but bert my was developed by Google
   researchers in Tensorflow. To solve this issue we have used Hugging Face platform to load the bert model. With the hugging face platform we can use Bert
   with Pytorch implementation. Here, we will talk about bert and how we build the modal with bert implementation.
   
   <img width="430" alt="bert" src="https://user-images.githubusercontent.com/64610564/175058890-5862fcf7-96b1-4cf9-9ff6-e757664404e4.PNG">

Same as before this model also build around three main classes “HatefulMemesDataset”, “LanguageAndVisionConcat” and “HatefulMemesModel”. These classes have unique work function. “HatefulMemesDataset” class is responsible for loading the data from different modalities and transform the data. When loading the data we have implemented Italian BERT model for each comment and return a Pytorch Tensor. Transform the image with torchVision and return a tensor.
At the end this class will return a dictionary with keys for each id, text, image and label. 

 We'll run our image information mode through a image model and result the last arrangement of element portrayals in
 our "LanguageAndVisionConcat" architecture, then do likewise for our language mode. Then we'll link these feature representations into another component vector, which we'll go through a fully connected layer for classification. 
 The language and vision modules will be utilized as parameters in our mid-level fusion model.
   
 <img width="368" alt="multimodal_modal" src="https://user-images.githubusercontent.com/64610564/175059828-e3383f70-0929-45ed-be3c-5d5390339fdb.PNG">     
      
Similar to first model I have trained my model in the same way. BERT embeddings, created as the text change in our data generator,
will be utilized as contribution for the language module. The language module's results will come from a trainable Linear layer, 
which will permit the embedding representation to be fine-tuned during training. The contributions to the vision module will be standardized image produced 
utilizing our data generator's image transform, and the results will be ResNet(He, et al., 2016) model outputs. HatefulMemesModel, which is a subclass of the
PyTorch Lightning pl, contains the code for training, early halting, checkpoint saving, and submission construction. 

# Result
As our model was big it took a lot of time to train our model. Just to run 1 epoch on Fasttext with ResNet took 1.5 hour and BERT with ResNet took 3 hour with only around 1500 train dataset in Google Colab. We initially had around 5027 datasets, however
I have implemented around 1500 dataset to train multimodal modal. But to train Unimodal Model I have used the 5027 datasets.
 We have got 50% accuracy for Multimodal fasttext with Resnet and 51% accuracy for Multimodal Bert with ResNet





   
   
