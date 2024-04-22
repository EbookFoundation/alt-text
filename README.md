# Alt-Text

A PyPi package used for finding, generating, and setting alt-text for images in HTML files.

Developed as a Computer Science Senior Design Project at [Stevens Institute of Technology](https://www.stevens.edu/) in collaboration with the [Free Ebook Foundation](https://ebookfoundation.org/).

[Learn more about the developers](#the-deveolpers).

## Getting Started

### Installation

You can find the PyPi package [here](https://pypi.org/project/alt-text/). To install the package via, you can execute the following in a terminal for your respective system...

Windows<br/>
`py -m pip install alt-text`

Unix/MacOS<br/>
`python3 -m pip install alt-text`

### Developer Dependencies

All developer dependencies can be found [here](#development-tools). You will only need to install these individually when working directly with the source code.

### Engine Dependencies

As of the moment, the image analyzation tools that Alt-Text uses are not fully bundled with the package itself. Hence, depending on the type of engines you are using (for Description Generation and/or Character Recognition), you will need to install various applications/get API keys for the respective functionalities.

#### Description Engines

Description Engines are used to generate descriptions of an image. If you are to use one of these, you will need to fulfill that specific Engine's dependencies before use.

##### ReplicateAPI

ReplicateAPI Engine uses the [Replicate API](https://replicate.com/), hence you will need to get an API key via [Logging in with Github](https://replicate.com/signin) on the Replicate website.

##### GoogleVertexAPI

GoogleVertexAPI Engine uses the [Vertex AI API](https://cloud.google.com/vertex-ai), hence you will need to get access from the [Google API Marketplace](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com). Additionally, Alt-Text uses Service Account Keys to get authenticated with Google Cloud, hence you will need to [Create a Service Account Key](https://cloud.google.com/iam/docs/keys-create-delete#creating) with permission for the Vertex AI API and have its according JSON.

##### BlipLocal

The BlipLocal Engine uses a modified version of the [cobanov/image-captioning repository](https://github.com/cobanov/image-captioning), which allows for the use of Blip locally via a CLI. To get started, you must download [this fork](https://github.com/xxmistacruzxx/image-captioning) of the repository and download/install the [BLIP-Large](https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large_caption.pth) checkpoint as described in the README.

#### OCR Engines

Optical Character Recognition Engines are used to find text within images. If you are to use one of these, you will need to fulfill that specific Engine's dependencies before use.

##### Tesseract

The Tesseract Engine uses [Tesseract](https://github.com/tesseract-ocr/tesseract), hence you will need to install the [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html).

#### Language Engines

Language Engines are used to generate a alt-text given an image description (from the [Description Engine](#Description-Engines)), characters found in an image (from the [OCR Engine](#OCR-Engines)), and context within the Ebook. If you are to use one of these, you will need to fulfill that specific Engine's dependencies before use.

##### OpenAI API

The OpenAI API Engine gives access to [Open AI's GPT Models via their API](https://platform.openai.com/docs/models). To use this, you will need an [API Key](https://openai.com/blog/openai-api) with access to the appropriate tier (more info on their [pricing page](https://openai.com/pricing)).

##### PrivateGPT

The PrivateGPT Engine gives allows for easy integration with an instance of [PrivateGPT](https://github.com/zylon-ai/private-gpt). To use this, you'll need a running instance of a [PrivateGPT API Server](https://docs.privategpt.dev/overview/welcome/introduction).

## Quickstart & Usage

### Setup

#### Standard Setup

The standard setup assumes that you have access to a [Description Engine](#Description-Engines) and [Language Engine](#Language-Engines) (the [OCR Engine](#OCR-Engines) being optional).

```python
from alttext.alttext import AltTextHTML

alt = AltTextHTML(
    ReplicateAPI("REPLICATE_KEY"),
    # Tesseract(),
    OpenAIAPI("OPENAI_KEY", "gpt-3.5-turbo"),
)
```

#### Legacy Setup

This setup assumes that you have access to a [Description Engine]() (the [OCR Engine]() and [Language Engine]() being optional).

```python
from alttext.alttext import AltTextHTML

alt = AltTextHTML(
    ReplicateAPI("REPLICATE_KEY"),
    # Tesseract(),
    # OpenAIAPI("OPENAI_KEY", "gpt-3.5-turbo"),
    options = {"version": 1}
)
```

#### Options

Below are the default options for the `AltTextHTML` class. You can change these by passing a `dict` into the `options` parameter during instantiation. When passing options, you only need the options you'd like to change from the default values in the `dict`.

```python
DEFOPTIONS = {
    "withContext": True,
    "withHash": True,
    "multiThreaded": True,
    "version": 2,
}
```

### Basic Usage

#### Loading an Ebook

```python
# from a file
alt.parseFile("/path/to/ebook.html")

# or from a string
alt.parse("<HTML>...</HTML>")
```

#### Getting Images

```python
# getting all images
imgs : list[bs4.element.Tag] = alt.getAllImgs()

# getting all images with no alt attribute or where alt = ""
imgs_noalt : list[bs4.element.Tag] = alt.getNoAltImgs()

# get a specific image by src
img : bs4.element.Tag = alt.getImg("path_as_in_html/image.png")
```

#### Generating Alt-Text

```python
# generate alt-text for a single image by src
alt_text : str = alt.genAltText("path_as_in_html/image.png")

# generate an association from an image tag
# example_association = {
#   "src" : "path_as_in_html/image.png"
#   "alt" : "generated alt text"
#   "hash" : 1234
# }
association : dict = alt.genAssociation(img : bs4.element.Tag)

# generate a list of associations given a list of image tags
associations : list[dict] = alt.genAltAssociations(imgs : list[bs4.element.Tag])
```

#### Setting Alt-Text

```python
# setting alt-text for a single image by src
new_img_tag : bs4.element.Tag = alt.setAlt("path_as_in_html/image.png", "new alt")

# setting alt-text for multiple images given a list of associations
new_img_tags : list[bs4.element.Tag] = alt.setAlts(associations : list[dict])
```

#### Exporting Current HTML Status

```python
# getting current html as string
html : str = alt.export()

# exporting to a file
path : str = alt.exportToFile("path/to/new_html.html")
```

## Our Mission

The Alt-Text project is developed for the [Free Ebook Foundation](https://ebookfoundation.org/) as a Senior Design Project at [Stevens Institute of Technology](https://www.stevens.edu/).

As Ebooks become a more prominant way to consume written materials, it only becomes more important for them to be accessible to all people. Alternative text (aka alt-text) in Ebooks are used as a way for people to understand images in Ebooks if they are unable to use images as intended (e.g. a visual impaired person using a screen reader to read an Ebook).

While this feature exists, it is still not fully utilized and many Ebooks lack alt-text in some, or even all their images. To illustrate this, the [Gutenberg Project](https://gutenberg.org/), the creator of the Ebook and now a distributor of Public Domain Ebooks, have over 70,000 Ebooks in their collection and of those, there are about 470,000 images without alt-text (not including images with insufficient alt-text).

The Alt-Text project's goal is to use the power of various AI technologies, such as machine vision and large language models, to craft a solution capable of assisting in the creation of alt-text for Ebooks, closing the accessibility gap and improving collections, such as the [Gutenberg Project](https://gutenberg.org/).

### Contact Information

The emails and relevant information of those involved in the Alt-Text project can be found below.

#### The Deveolpers

- Jack Byrne
  - jbyrne4@stevens.edu
- David Cruz
  - da.cruz@aol.com
  - [David's Website](https://xxmistacruzxx.github.io/)
  - [David's Github](https://github.com/xxmistacruzxx)
  - [David's LinkedIn](https://www.linkedin.com/in/davidalexandercruz/)
- Jared Donnelly
  - jdonnel3@stevens.edu
- Ethan Kleschinsky
  - ekleschi@stevens.edu
- Tyler Lane
  - tlane@stevens.edu
- Carson Lee
  - clee27@stevens.edu

#### The Client

- Eric Hellman
  - eric@hellman.net

#### Advisor

- Aaron Klappholz
  - aklappho@stevens.edu

## APIs, Tools, & Libraries Used

Alt-Text is developed using an assortment of tools...

### Development Tools

Alt-Text is developed using...

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [EbookLib](https://pypi.org/project/EbookLib/)
- [Replicate](https://pypi.org/project/replicate/)
- [Google-Cloud-AIPlatform](https://pypi.org/project/google-cloud-aiplatform/)
- [PyTorch](https://pypi.org/project/torch/)
- [PyTesseract](https://pypi.org/project/pytesseract/)
- [OpenAI Python API](https://pypi.org/project/openai/)

### APIs and Supplementary Tools

- [Replicate API](https://replicate.com/)
- [Vertex AI API](https://cloud.google.com/vertex-ai)
- [cobanov/image-captioning](https://github.com/cobanov/image-captioning)
- [Tesseract](https://github.com/tesseract-ocr/tesseract)
- [OpenAI API](https://openai.com/blog/openai-api)
- [PrivateGPT](https://github.com/zylon-ai/private-gpt)

### Packaging/Distribution Tools

Alt-Text is distributed using...

- [PyPi](https://pypi.org/)
- [Hatchling](https://pypi.org/project/hatchling/)
