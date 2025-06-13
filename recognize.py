from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
import os



load_dotenv()


endpoint = os.getenv("ENDPOINT")
key = os.getenv("KEY")

filePath = "https://storageformrecognized.blob.core.windows.net/container/sample-invoice.pdf"
fileLocale = "en-US"
fileModelId = "prebuilt-invoice"

print(f"\n Polonczenie z Forms Recognizer: {endpoint}")
print(f"Analiza faktury: {filePath}")


document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


poller = document_analysis_client.begin_analyze_document_from_url(
    fileModelId, filePath, locale=fileLocale
)


receipts = poller.result()

for idx, receipt in enumerate(receipts.documents):

    vendor_name = receipt.fields.get("VendorName")
    if vendor_name:
        print(f"\nNazwa sprzedawcy: {vendor_name.value}, with confidence {vendor_name.confidence}.")


    customer_name = receipt.fields.get("CustomerName")
    if customer_name:
        print(f"Nazwa klienta: '{customer_name.value}, with confidence {customer_name.confidence}.")


    invoice_total = receipt.fields.get("InvoiceTotal")
    if invoice_total:
        print(f"Suma faktury: '{invoice_total.value.symbol}{invoice_total.value.amount}, with confidence {invoice_total.confidence}.")

print("\nAnaliza skończona\n")