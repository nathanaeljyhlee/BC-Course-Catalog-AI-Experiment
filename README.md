## **Project Checklist**

### **1. Extract and Clean Course Data**

- [x]  Split your PDF catalog into ≤1,000-page parts (e.g., with PyPDF2).
- [x]  Upload each part to Mistral Document AI.
- [x]  Download and save each JSON result 
- [X]  Write a Python script to extract course titles and descriptions from all JSONs.
- [x]  Save to a single CSV (e.g., `courses.csv`) with columns: `course_title`, `course_description`. [1 of 7!]

---
SKIPPED
### **2. Prepare the UM-CAI-Fellowship Code**

- [ ]  Fork or clone [the repo](https://github.com/hughvd/UM-CAI-Fellowship) into your Replit or local workspace.
- [ ]  Install required dependencies (see their README or `requirements.txt`).
- [ ]  Review sample input CSVs/notebooks to confirm expected format.

---
MOVED TO GOOGLE COLAB
### **3. Adapt for Your Data and (if needed) Mistral APIs**

- [ ]  Test their pipeline with your `courses.csv` as input.
- [ ]  If you want to use Mistral Embedding/LLM APIs:
    - [ ]  Replace OpenAI API calls with Mistral equivalents in the scripts (I can help you identify where).
    - [ ]  Confirm API responses/embedding vector shapes match.
- [ ]  Adjust column references if their code expects different names.

---

### **4. Run and Validate**
VALIDATED
- [ ]  Run a sample query (e.g., “AI and ethics”) through the pipeline.
- [ ]  Review and interpret the top recommended courses.
- [ ]  Export or save results as CSV, and/or adapt for further use (reporting, UI, etc.).

---

### **5. (Optional) Build a Simple UI**

- [ ]  (If desired) Wrap the pipeline in a Streamlit or simple web app for others to use.
