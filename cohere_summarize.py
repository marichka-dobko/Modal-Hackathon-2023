import cohere
import time
import pandas as pd
# Paste your API key here. Remember to not share it publicly
api_key = ''
co = cohere.Client(api_key)

from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('/Users/mariadobko/Downloads/Plans pdfs/silverprime.pdf')
# getting a specific page from the pdf file
page = reader.pages[0]
# extracting text from page
text = page.extract_text()

# text = 'You may have access to Oscar’s $0 unlimited virtual primary care services—even if you haven’t hit your deductible. Depending on your plan, prescriptions and labs will also cost you $0, if they’re ordered by your Oscar Virtual Primary Care team.* Please refer to your plan documents for more information. *For prescriptions and lab savings to apply, they must be prescribed by your Oscar Virtual Primary Care provider under certain Silver, Gold or Platinum plans. Additional plan highlights include: Step tracking rewards for staying active; No referrals required; Single-tier EPO network; and Embedded deductibles.'

response = co.summarize(
    text=text,
    model='command',
    length='medium',
    extractiveness='medium'
)

summary = response.summary
print(summary)
