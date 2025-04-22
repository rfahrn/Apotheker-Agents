# dowladed form  csv  blob:https://dps.fda.gov/68aad9ca-1fe4-4414-937e-49f75b71f5d2 (hopefully this is always updated not sure )
# process_medicaiton_guides.py 

import os
import requests
import pandas as pd
from tqdm import tqdm
from langchain_community.document_loaders import PyPDFLoader
import argparse


def download_pdf(url, appl_no, output_dir):
    try:
        url = url.split("#")[0]
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        local_path = os.path.join(output_dir, f"{appl_no}.pdf")
        with open(local_path, "wb") as f:
            f.write(response.content)
        return local_path
    except Exception as e:
        return f"[Error: Download failed - {e}]"


def extract_text_with_langchain(pdf_path):
    try:
        loader = PyPDFLoader(pdf_path, mode="single", pages_delimiter="Reference ID:")
        docs = loader.load()
        full_text = "\n\n".join(doc.page_content.strip() for doc in docs if doc.page_content)
        return full_text if full_text.strip() else "[Empty PDF]"
    except Exception as e:
        return f"[Error: Extraction failed - {e}]"


def process_guides(csv_path, pdf_dir, txt_dir):
    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    df['Appl. No.'] = df['Appl. No.'].astype(str)

    results = []

    for idx, row in tqdm(df.iterrows(), total=len(df), desc="📄 Processing PDFs"):
        appl_no = row['Appl. No.']
        url = row['URL']
        pdf_path = download_pdf(url, appl_no, pdf_dir)
        if pdf_path.startswith("[Error"):
            print(f"❌ Download failed for Appl. No. {appl_no}")
            results.append({"appl_no": appl_no, "text": pdf_path})
            continue
        extracted_text = extract_text_with_langchain(pdf_path)
        txt_file_path = os.path.join(txt_dir, f"{appl_no}.txt")
        with open(txt_file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        results.append({"appl_no": appl_no, "text": extracted_text[:200] + "..."})

    print("\n All Medication Guide PDFs processed.")
    return results


def main():
    parser = argparse.ArgumentParser(description="Download and extract text from Medication Guide PDFs.")
    parser.add_argument("--csv", required=True, help="Path to the Medication Guides CSV file.")
    parser.add_argument("--pdf_dir", default="pdfs", help="Directory to save downloaded PDFs.")
    parser.add_argument("--txt_dir", default="texts", help="Directory to save extracted text files.")
    args = parser.parse_args()
    process_guides(args.csv, args.pdf_dir, args.txt_dir)


if __name__ == "__main__":
    main()

# use : python create_db.py --csv "C:\Users\FahRe\Downloads\Medication Guides.csv" --pdf_dir pdfs --txt_dir texts

