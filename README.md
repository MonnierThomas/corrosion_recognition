# Image recognition with corrosion marks in industrial environment  

> This GitHub repository is a project made in partnership with DI Africa, and supervised by Mines Paris. We implemented a CNN in order to identify marks of corrosion on pictures of oil platforms.

<p align="center">
  <img src="https://media-exp1.licdn.com/dms/image/C560BAQGsupEBelRQfA/company-logo_200_200/0/1584626088075?e=2159024400&v=beta&t=1rQWcrc8ncZZ0BupAiuaNhz2SUHiJCfNdWAdu9ScGxw" />
</p>

# Table of Contents

- [Introduction](#introduction)
- [DI Africa](#di-africa)
- [Methods](#methods)
- - [Reasoning](#reasoning)
- - [Image Scraping](#image-scraping)
- - [Image Processing](#image-processing)
- - [CNN Implementation](#cnn-implementation)
- [Results](#results)
- [Discussion](#discussion)
- [Conclusion](#conclusion)
- [Special Thanks](#special-thanks)
- [References](#references)

# Introduction

Our second semester computer science project at Mines Paris was proposed to us by Bertrand Duvivier and Christophe Lemerle. They both work at DI Africa, a start-up dealing with oil platforms on the African coast, and therefore interested in their maintenance. In order to solve the problem of corrosion of materials used on the platforms and to prevent expensive repairs and maintenance, DI Africa contacted Mines Paris to obtain a means of automatic detection of corrosion marks on materials in industrial environment.

Our engineering group (Ambroise Favre, Charlotte de Mailly Nesle, Thomas Monnier) had two objectives:
- to process the images according to a binary classification of the materials (0: not corroded, 1: corroded)
- to quantify the degree of corrosion of the material

Unfortunately, the second objective was quickly discarded in favor of the first. Indeed, quantifying the degree of corrosion of a material using Machine Learning algorithms seems almost impossible given the number of variables involved. The most obvious one - the degree of corrosion of a material depends on the distance from which it is photographed - convinced us that it was better to concentrate on the first objective.

Thus, we chose to use Artificial Intelligence tools to detect corrosion marks on materials according to a binary classification.

# DI Africa

> Extract from the topic description

[DI Africa](https://www.linkedin.com/company/di-africa) provides international technical assistance, i.e. DI Africa send engineers and technicians to their clients' industrial sites. Their core business is oil & gas in Africa and clients' sites are often offshore platforms. We also intervene in other sectors such as mining, energy, nuclear, construction or heavy industry in the broad sense or on other continents. We have been in existence since November 2019 and are currently established in Mauritius and Gabon, with other countries being opened. Two former students from Mines Paris, including Bertrand Duvivier, are co-founders.

# Methods

## Reasoning

In order to meet our objective, we had to know what we needed to address and answer the following questions: 

> What problem are we facing? 
> What Machine Learning algorithms can we use? 
> What is the best choice to process the images?

Despite the large number of Machine Learning algorithms that are used in industry, one in particular interested us: the CNN (Convolution Neural Network). Why?

We are dealing with :
- a two-class classification problem (uncorroded and corroded)
- an image processing problem 

A supervised algorithm like the CNN seems appropriate, especially since it is known for its accuracy (which we will evaluate by the F1-score).

## Image Scraping

[Algorithm:](src/image_scraping/image_scraping.py) `src/image_scraping/image_scraping.py`

In order to use a CNN, we must have a dataset to train, test and validate our algorithm. Problem is, DI Africa does not have a database with images of corroded and uncorroded materials. Besides, websites collecting datasets all over the globe such as Kaggle are missing corrosion / uncorrosion dataset. As such dataset is unavailable, we must therefore succeed in downloading images from the web in order to have our own database. The first approach was to retrieve an amount of data of about 2,000 images (1,000 images of corroded materials, 1,000 images of uncorroded materials). Sadly, we are not able to share our collected dataset for obvious private reasons.

To do so, we used a webdriver, the Selenium module and we wrote an algorithm to download images by keywords from Google Images (script_ruler.py). Among the keywords we used:
- corrosion
- corroded materials
- corroded steel
- steel
- *lots of different metals*

The webdriver can be found in [src/image_scraping/chromedriver_linux64.zip](src/image_scraping/chromedriver_linux64.zip).
Careful: You should use a webdriver that fits your Chrome version. Find all chromedriver versions [here](https://chromedriver.chromium.org/)

Then, follow these steps:
```
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

Check if your chromedriver has correctly been installed and ready to use:
`chromedriver --version`

To use the script:
```
usage: image_scraping.py [-h] -k KEYWORDS [KEYWORDS ...]

optional arguments:
  -h, --help            show this help message and exit
  -k KEYWORDS [KEYWORDS ...], --keywords KEYWORDS [KEYWORDS ...]
                        keywords
```
For example: `python3 image_scraping.py -k 'corroded steel' 'corrosion'`

From there, we had to deal with inconsistent images (not matching the terms *uncorroded* and *corroded*, schematics, etc).

## Image Processing

[Algorithms:](src/image_processing/) `src/image_processing/`

Now that we have our database, we had to format and size the images in order to have them all of the same quality and size in order to be able to use the CNN.

We also have to create three batches of images: one for training, one for validation and one for testing. Overall, the distribution is as follows:
- 80% of the images go to training and validation, respectively divided into 80% and 20%.
- 20% of the images go to testing

However, a CNN needs large amount of data to be efficient. To enhance our dataset (which consists of only 2,000 images), we used common strategies in Machine Learning: symmetrize our images, which allowed us to have 4 times more data than before.

## CNN Implementation

[Algorithm:](src/cnn.py) `src/cnn.py`

After coding the CNN, we proceeded to several corrosion mark recognition tests on our test images. Unfortunately, the results were not good. The performance of the algorithm was not very good (around 0.6 of accuracy). Lots of parameters could actually be changed to improve the results of the CNN. To overcome these problems, we resorted to symmetrizing the images, modifying the quality of the images, and removing a layer (because of overfitting).

# Results

Finally, despite spending some time on fine-tuning the model, we obtained a F1-score of 0.7, which is unfortunately not enough for the use that our employers want to make of it. 

One positive point: the model has a high recall. Indeed, the results of our last model show that when it says that an image does not show traces of corrosion, we can be sure that the material does not have any, which is rather positive and already saves time for maintenance.

# Discussion

We encountered several issues throughout our project that may explain the disappointing F1-score:
- the lack of a labelled dataset of corroded / uncorroded materials
- the low amount of data that we used for training and validation
- the low quality of the data we used
- the little time spent on modyfing hyperparameters and tuning

# Conclusion

Our algorithm works. All that remains is to have a database with a few million professional images of corroded and non-corroded materials used by the start-up to have any hope of obtaining an accuracy close to 0.95.

# Special Thanks

We warmly thank Bertrand Duvivier and Christophe Lemerle for their support, their weekly help and the subject proposal which really allowed us to discover and learn more about Deep Learning and Image Processing.

# References

[Project Instructions](topic/)
