# Tested for gif, jpeg, png 
def extract_image_text_by_url(url):
    # Be sure to set GOOGLE_APPLICATION_CREDENTIALS env var
    # 1000 Requests per month for free
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = url

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    description = []

    for text in texts:
        description.append(text.description)
    
    return description[0]

def extract_pdf_by_url(url):
    import pdfplumber
    import urllib3
    import io

    http = urllib3.PoolManager()
    temp = io.BytesIO()
    temp.write(http.request("GET", url).data)
    all_text = ''

    with pdfplumber.open(temp) as pdf:
        # CODE FOR FIRST PAGE
        page = pdf.pages[0]
        all_text = page.extract_text()
        # CODE FOR ALL PAGES:
            # for pdf_page in pdf.pages:
            #     single_page_text = pdf_page.extract_text()
            #     all_text = all_text + '\n' + single_page_text
    return all_text

print(extract_image_text_by_url('https://cdn0.tnwcdn.com/wp-content/blogs.dir/1/files/2015/09/giphy-1.gif')) 
print(extract_pdf_by_url('https://alex.smola.org/drafts/thebook.pdf'))

# TODO: OCR on PDF rather than extracting text (ie. for scanned PDFs)
# TODO: Error checking