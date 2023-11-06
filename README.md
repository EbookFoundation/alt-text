# Alt-Text

A PyPi package used for finding, generating, and setting alt-text for images in HTML and EPUB files.

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

##### ReplicateMiniGPT4API

ReplicateMiniGPT4API Engine uses the [Replicate API](https://replicate.com/), hence you will need to get an API key via [Logging in with Github](https://replicate.com/signin) on the Replicate website.

##### GoogleVertexAPI

GoogleVertexAPI Engine uses the [Vertex AI API](https://cloud.google.com/vertex-ai), hence you will need to get access from the [Google API Marketplace](https://console.cloud.google.com/marketplace/product/google/aiplatform.googleapis.com). Additionally, Alt-Text uses Service Account Keys to get authenticated with Google Cloud, hence you will need to [Create a Service Account Key](https://cloud.google.com/iam/docs/keys-create-delete#creating) with permission for the Vertex AI API and have its according JSON.

#### OCR Engines

Optical Character Recognition Engines are used to find text within images. If you are to use one of these, you will need to fulfill that specific Engine's dependencies before use.

##### Tesseract

The Tesseract Engine uses [Tesseract](https://github.com/tesseract-ocr/tesseract), hence you will need to install the [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html).

## Quickstart & Usage

To be added...

## Our Mission

The Alt-Text project is developed for the [Free Ebook Foundation](https://ebookfoundation.org/) as a Senior Design Project at [Stevens Institute of Technology](https://www.stevens.edu/).

As Ebooks become a more prominant way to consume written materials, it only becomes more important for them to be accessible to all people. Alternative text (aka alt-text) in Ebooks are used as a way for people to understand images in Ebooks if they are unable to use images as intended (e.g. a visual impaired person using a screen reader to read an Ebook).

While this feature exists, it is still not fully utilized and many Ebooks lack alt-text in some, or even all their images. To illustrate this, the [Gutenberg Project](https://gutenberg.org/), the creator of the Ebook and now a distributor of Public Domain Ebooks, have over 70,000 Ebooks in their collection and of those, there are about 470,000 images without alt-text.

The Alt-Text project's goal is to use the power of AI, Automation, and the Internet to craft a solution capable of automatically generating descriptions for images lacking alt-text in Ebooks, closing the accessibility gap and improving collections, such as the [Gutenberg Project](https://gutenberg.org/).

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

Alt-Text is developed using an assortment of modern Python tools...

### Development Tools

Alt-Text is developed using...

- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [EbookLib](https://pypi.org/project/EbookLib/)
- [Replicate](https://pypi.org/project/replicate/)
- [Google-Cloud-AIPlatform](https://pypi.org/project/google-cloud-aiplatform/)
- [PyTesseract](https://pypi.org/project/pytesseract/)

### APIs and Supplementary Tools

- [Replicate API](https://replicate.com/)
- [Vertex AI API](https://cloud.google.com/vertex-ai)
- [Tesseract](https://github.com/tesseract-ocr/tesseract)

### Packaging/Distribution Tools

Alt-Text is distributed using...

- [PyPi](https://pypi.org/)
- [Hatchling](https://pypi.org/project/hatchling/)
