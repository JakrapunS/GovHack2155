# GovHack 2023

## Team members

<table>
  <tr>
   <td>Jakrapun Sangchan
   </td>
   <td> <a href="mailto:jakrapun.san@gmail.com">jakrapun.san@gmail.com</a>
   </td>
  </tr>
  <tr>
   <td>Ajay Krishnan Jayakumar Usha
   </td>
   <td>  <a href="mailto:ajaykrishnan.ju@gmail.com">ajaykrishnan.ju@gmail.com</a>
   </td>
  </tr>
  <tr>
   <td>Kristian Guinto
   </td>
   <td><a href="mailto:guintojames8@gmail.com">guintojames8@gmail.com</a>
   </td>
  </tr>
</table>



## Project overview

<table>
  <tr>
   <td>Project Title
   </td>
   <td><a href="https://hackerspace.govhack.org/challenges/tagging_photographic_images_showcasing_the_magnificent_history_of_victoria">Tagging photographic images: showcasing the magnificent history of Victoria</a>
   </td>
  </tr>
  <tr>
   <td>State
   </td>
   <td>Victoria
   </td>
  </tr>
  <tr>
   <td>Sponsor
   </td>
   <td>Public Record Office Victoria (PROV)
   </td>
  </tr>
  <tr>
   <td>Project objective
   </td>
   <td>Using new technologies and tools, crowdsource, or other ways to tag images so that they can be used on the PROV website.
   </td>
  </tr>
  <tr>
   <td>Solution Summary
   </td>
   <td>Use generative ai to automatically make captions and tags and have humans in the loop to enhance the model output.
   </td>
  </tr>
  <tr>
   <td>Dataset
   </td>
   <td>Images from:
<p>
 <a href="https://prov.vic.gov.au/explore-collection/photographic-collections">https://prov.vic.gov.au/explore-collection/photographic-collections</a>
<p>
Metadata from: <a href="https://prov.vic.gov.au/prov-collection-api">https://prov.vic.gov.au/prov-collection-api</a>
   </td>
  </tr>
  <tr>
   <td>Repository
   </td>
   <td><a href="https://github.com/JakrapunS/GovHack2155/tree/main">Github</a>
   </td>
  </tr>
</table>



## Solution description and data story 

### Objective



* The project’s primary objective is to find new ways to improve PROV’s search functionality. 


### Solution



* Generate new metadata describing an image to expand its searchability. The metadata that we generate is a combination of a caption and responses to questions about the image (tags). 
* An app combining generative ai models and human feedback to generate correct and relevant image captions and tags. 
* A dataset that will allow for future development by taking advantage of techniques such as model fine-tuning and [Reinforcement learning from human feedback (RLHF)](https://huyenchip.com/2023/05/02/rlhf.htmlhttps://huyenchip.com/2023/05/02/rlhf.html), a technique used in improving ChatGPT’s performance. 




### Technical description

Our proposed solution can be divided into several components including:



1. Using public APIs to access image data. 
2. Using state-of-the-art generative ai models to automatically make image captions and tags. 
3. An app that puts humans in the loop to enhance the model’s outputs. 
4. A demonstration of how the refined data can be used to self-improve.

*Using public APIs to access image data*

This section includes a data pipeline written in Python using the PROV API to collect image links and descriptions. The pipeline allows the user to query either on serial number or keyword. 

*Using state-of-the-art generative ai models to automatically make image captions and tags.*

For our machine learning project, we chose to work with the BLIP model, an open-source vision-language model from Salesforce. We focused on two main tasks:

1. Image Captioning
2. Image Tag Generation

Using the BLIP model, we generated captions for images retrieved from the PROV API. For generating tags, we applied BLIP's Visual Question Answering capability. This allowed the model to answer a set of predefined questions and provide corresponding tags. Future iterations of this project can have more context-specific questions to generate context-specific tags. 

In our implementation, we refrained from using third-party APIs. Instead, we downloaded the model and executed it locally within our environment. This approach ensured that no data was transmitted outside the system, thereby preventing potential data leakage to the public.

 

*An app that puts humans in the loop to enhance the model’s outputs*

Our app has the following functionalities:

* Keyword search on PROV’s image repository. The search will load images using the API. 
* Interactive presentation of the model-generated description and tags. 
* Generate descriptions and tags from any image URL. 

*A demonstration of how the refined data can be used to self-improve*

In this section, we've adopted principles from [Reinforcement Learning from Human Feedback](https://huyenchip.com/2023/05/02/rlhf.html#language_model) (RLHF). The essence of this approach is to collect user feedback to elevate our model's performance in subsequent iterations. We've designed an intuitive user interface that facilitates users in providing feedback and making adjustments to model outputs. By leveraging this feedback, we aim to accumulate more accurate descriptions and tags, setting the stage for enhanced model performance in the future.

The combination of these four components gives a complete solution while also providing a systematic way for self-improvement. The refined captions and tags can be added to the metadata of the images which will allow for better searchability. These can also be used to improve the model’s performance such that it is more aligned with the objectives of an organization.