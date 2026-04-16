🌐 AI Translator Dashboard

A modern AI-powered translation web app built with Streamlit and powered by Azure Cognitive Services.
Translate text in real-time across 100+ languages with a beautiful dashboard UI.

🚀 Features
🌍 Translate text into 100+ languages
🔍 Auto-detect source language
⚡ Real-time translation using Azure API
📊 Dashboard analytics (translations, characters, languages)
📜 Translation history tracking
🎨 Modern glassmorphism UI with animations
🛠️ Tech Stack
Frontend: Streamlit
Backend: Python
API: Azure Translator API
Libraries:
streamlit
requests
uuid
collections

⚙️ Installation
1. Clone the repository
git clone https://github.com/rishabh-tiwari45/azure-translator-dashboard.git
cd azure-translator-dashboard
2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3. Install dependencies
pip install -r requirements.txt
▶️ Run the App
streamlit run app.py
🔑 Azure Setup
Go to https://portal.azure.com
Create a Translator Resource
Copy:
API Key
Region (e.g., eastus)
Paste them in the app sidebar
📂 Project Structure
azure-translator-dashboard/
│── app.py
│── requirements.txt
│── README.md
🔄 How It Works
User Input → Streamlit UI → Azure API → Translation → Output

📸 Screenshot
<img width="2834" height="1622" alt="image" src="https://github.com/user-attachments/assets/3a1c4fe3-26c1-4cc8-972f-da005a739b97" />




⚠️ Notes
Make sure your Azure API key is valid
Internet connection required
Avoid exceeding API rate limits
📈 Future Improvements
🎤 Voice translation
📄 File translation (PDF, DOCX)
☁️ Deployment (Streamlit Cloud / AWS)
💾 Database for history
👨‍💻 Author

Rishabh Tiwari

⭐ Support

If you like this project, give it a ⭐ on GitHub!
