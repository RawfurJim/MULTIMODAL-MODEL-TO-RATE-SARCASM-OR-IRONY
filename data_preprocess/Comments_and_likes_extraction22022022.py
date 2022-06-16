# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 10:35:58 2022

@author: meval
"""

# Importing necessary libraries
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'                                       # to fix the issue OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.

import cv2 as cv                                                                # To import the images and sharpening them for better text detection.
import numpy as np                                                              # To create a kernal for image sharpening.
import easyocr                                                                  # A python package to extract texts from image.
import os                                                                       # This module in python provides functions to interact with operating system. For example: To move files across the directories, listing out files and directories, deleting directory or files and many more.
import re                                                                       # Regex library for separating likes and comments from extracted texts. Also, for removing any special/unwanted characters. 
import pandas as pd                                                             # To create DataFrame.
import itertools                                                                # To repeat any element in the list n times.

reader=easyocr.Reader(['it'])                                                   # EasyOCR supports multiple languages. Since, in our case, the text is in Italian, so for that downloaded the specific text recognition model.


src=r'C:\Users\HP\Desktop\sample_dissertation\Archivio parte_2\redbox' 
srcfiles=os.listdir(src)


list1=[]                                                                        # Empty list to store the extracted text.
for photo in srcfiles:
    photopath=os.path.join(src, photo)  
    img=cv.imread(photopath,cv.IMREAD_UNCHANGED)                                # Loads an image from specified path(photopath).
                    
    kernal=np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])                          # Defined a 3x3 kernal that convolves with the image. 
    sharpened = cv.filter2D(img,-1,kernal)                                      # This function convolves an above defined kernal with an image. During this process the kernal adds contrast around an edge by accentuating bright and dark areas thus making the image more sharper. 
    
    extracted_text=reader.readtext(sharpened, paragraph=True, text_threshold=0.6, low_text=0.4, detail=0)  # The sharpened image is fed into the text recognition model for text extraction. 
    listing=[]                                                                  
    listing.append(' '.join(extracted_text))                                    


    if re.findall('Piace\s+a\s+[0-9]+\s+persone|Piace\s+[0-9]+\s+persone|Mi\s+piace\s+.*\s*[0-9]+',listing[0]):  
      list1.append([listing[0]])                                                # Storing the extracted texts into the list1
    else:
      list1.append(extracted_text)                                              # Storing the extracted texts into the list1
      
      
#####################################################################################################################################################################################################################################################################################
# The list1 contains extracted text inside a nested list (i.e. each element in list1 is also a list that includes the extracted text within) which is not in the proper format to do any further processing. 
# Some nested list contains text in a single string format while other contains text in multiple string format. Below is a code that correctly formats the list so that each nested list includes extracted
# text in a single string format and stores it in the another list named:- text_list.

formatted_list=[]                                                               # Empty list to store the properly formatted texts

for i in list1:
  if len(i)==1:                                                                 # If the nested list inside the list1 contains extracted text in a single string format, then directly appending that nested list to the formatted_list.
    formatted_list.append(i)                                                    

  if len(i)==2:                                                                 # If the nested list inside the list1 contains extracted text in the form of 2 strings format then:-
    try:
      if float(i[1]):                                                                        # If 2nd string is a number, joining both the string togather by space and then appending that nested list to the formatted_list
        formatted_list.append([' '.join(i)])
    except:
      formatted_list.append(['|'.join(i)])                                                   # If 2nd string is not a number, joining both the string togather by "|" and then appending that nested list to the formatted_list

  if len(i)>2:                                                                  # If the nested list inside the list1, contains extracted text in the form of more than 2 strings then:-
    t=len(i)
    joining=[]
    correctcmnt=[]
     
    for count in range(t-1):
      try:
        if float(i[count+1]):
          lst=[i[count],i[count+1]]
          joining.append(' Likes: '.join(lst))                                               # Joining all the strings togather by the word "Likes:" and then appending that nested list to the formatted_list
      except:
        lst=[i[count],i[count+1]]
        joining.append(' Likes: '.join(lst))
    
    for i in joining:

      pattrn=re.compile('Likes:\s+.\s*[0-9]+\.*[0-9]+|Likes:\s+[0-9]+\.*[0-9]+|Likes:\s+[0-9]+.')
      if re.findall(pattrn,i):
        correctcmnt.append(i)
   
    formatted_list.append([' '.join(correctcmnt)])
    
######################################################################################################################################################################################################################################################################################
# The formatted_list contains properly formatted text inside a nested list. The Below code removes these nestings and then stores the output in another list named:- text_list.

text_list=[]
def removeNestings(l):
    for i in l:
        if type(i) == list:
            removeNestings(i)
        else:
            text_list.append(i)
removeNestings(formatted_list)
for i in range(len(text_list)):
  v=re.findall('Piace\s+a\s+[0-9]+\s+persone\s+.[0-9A-Za-z]+$|Piace\s+a\s+[0-9]+\s+persone\s+[0-9A-Za-z]+$',text_list[i]) 
  for p in v:
    b=p.split()
    b=b[:-1]
    j=' '.join(b)
    text_list[i]=text_list[i].replace(p,j)
    
# The extracted texts contain likes in a different format such as ('Piace a 176 persone','Mi piace 339','1.5 mila','456', and 'Likes: 453') 
# The below code detects all these different formats and seperates these likes from rest of the extracted texts.

imagename=srcfiles
commentbox=[]                                                                   # Stores the images name.
likes=[]                                                                        # Stores the seperated likes.
list4=[]
comments=[]                                                                     # Stores the comments.
for text in text_list:
  patterns=[                                                                    # List of regex patterns to detect the likes present in the extracted texts.
            '[0-9]+\.*,*[0-9]+$',
            '\sPiace\s+a\s+[0-9]+\s+persone',
            '\sPiace\s+a\s+[0-9]+\s+Dersone',
            '\sPiace\s+[0-9]+\s+persone',
            '\sPíacea*\s+[0-9]+\s+persone',
            '\sPiace a 550 persone\s+.[0-9]',
            '\sPíace\s+a*\s*persone',
            '\sPiace\s+a*\s*persone',
            'Piacea\s+[0-9]+\s+persone',
            '[0-9,.]+\s+mila',
            '\sPíace\s+a\s+[0-9]+\s+persone',
            '\sPiace\s+à\s+[0-9]+\s+persone',
            '\sMí\s+piace\s+[0-9]+',
            '\sMi\s+piace\s+[0-9]+\s+[0-9]+',
            '\sMi\s+piace\s+[0-9]{0,3}[a-zÉG*&]+\s+[0-9]+\.*,*[0-9]+',
            '\sMi\s+piace\s+[0-9]+\.*,*[0-9]+',
            '\sMi\s+piace\s+[0-9]+',
            '\sMi\s+piace\s+[0-9]*[a-z]+\s+[0-9]+',
            '\sMi\s+piace\s+.\s+[0-9]+',
            'Likes:\s+[0-9]+[a-z]+',
            'Likes:\s+[0-9]+\.*,*[0-9]+[a-z]+',
            'Likes: [0-9]+.[0-9]+',
            'Likes:\s+.\s*[0-9]+\.*,*[0-9]+[a-z]+',
            'Likes:\s+\'[0-9]+\.*,*[0-9]+',           
            'Likes: [0-9]+\.*,*[0-9]+',
            'Likes:\s+[0-9]+\.*,*[0-9]+[a-z]+',
            'Likes:\s+[0-9]+',
            '[0-9]+\.*,*[0-9]+$'
         ]  
  patternstring='|'.join(patterns)
  reg=re.compile(patternstring,re.IGNORECASE)
  pat=re.findall(reg,text)                                                      # Regex function for detecting the likes.
  if not pat:
    pat.append('Unable to extract')                                             # In case no like is detected in particular comment
  
  
  list4.append(pat)
  updtstr=text
  for j in range(len(pat)):                                                     # Seperating the likes from rest of the texts.
    t=updtstr.split(pat[j])
    updtstr=' 228001 '.join(t)
  l=updtstr.split(' 228001 ')
  l=list(filter(None,l))
  for i in range(len(l)):
    likes.append(pat[i])                                                        # Storing the seperated likes into the list named: likes
    comments.append(l[i])                                                       # Storing the rest of the texts into the list named: comments

count=0                                                                         # To keep the track of which comment belongs to which image, storing the images name in the list named: commentbox
for i in imagename:
  commentbox.append(list(itertools.repeat(i,len(list4[count]))))
  count=count+1

flatList = [ item for elem in commentbox for item in elem]
final=[[i,j,k] for i,j,k in zip(flatList,comments,likes )]                      # This is the final list containing nested list of [images name, comments, likes]

##########################################################################################################################################################################################################################
# Creating a DataFrame using the final list to store all the extracted information in tabular form.

df=pd.DataFrame(final,columns=['Image','Comment','Raw_Likes'])

# The formed DataFrame contains some unwanted rows(rows with no comments, improperly extracted comments). Removing all these rows from the DataFrame.

df=df[df['Raw_Likes']!='Unable to extract']
length=[]
for i in df['Comment']:
  length.append(len(i))
df['Comments_Length']=length
df=df[df['Comments_Length']>11]

###########################################################################################################################################################################################################################
# Some of the likes in the Raw_Likes column contains unwanted characters in them. The below code cleans these likes. 

remove=[]
for i in df['Raw_Likes']:
  pattern=re.compile(r'Píace\s+a*\s*persone|Piace\s+a*\s*persone',re.IGNORECASE)
  v= re.findall(pattern,i)
  if v:
    remove.append(v[0])    
  else:
    remove.append('none')

df['Unwanted_likes']=remove
df=df[df['Unwanted_likes']=='none']
likes=[]
for i in df['Raw_Likes']:
  likes.append(i)
like2=likes
for i in range(len(like2)):
  like2[i]=like2[i].replace('Likes:','').replace('\'','').replace(',','.')
for i in range(len(like2)):
  pattern=re.compile(r'Mi\s+piace\s+[0-9]{0,3}[a-zÉG*&]+\s+[0-9]+\.*,*[0-9]+|Mi\s+piace\s+[0-9]*[a-z]+\s+[0-9]+|Mi\s+piace\s+.\s+[0-9]+',re.IGNORECASE)
  v=re.findall(pattern,like2[i])
  if v:
    t=v[0].split()
    t.pop(2)
    like2[i]=like2[i].replace(v[0],' '.join(t))
df['Likes']=like2

############################################################################################################################################################################################################################
# Sorted the entire DataFrame in ascending order by the column: "Image"

df['sort']=df['Image'].str.extract('(\d+)', expand=False).astype(int)
df=df.sort_values('sort')
df=df.drop(['Raw_Likes','Comments_Length','Unwanted_likes','sort'],axis=1)

df                                                                              # The final DataFrame    

df.to_csv('Extracted_comments_and_likes.csv',index=False)      # Saving the Dataframe as CSV file 