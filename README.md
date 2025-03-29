# 🖼️ ImageInsight AI: Multimodal Image Analysis  

## 🔬 Advanced AI for Visual Intelligence  

**ImageInsight AI** is an enterprise-grade application leveraging **Google's Gemini foundation models** to provide sophisticated image analysis and insights. Development began on **February 11, 2024**, with the goal of building a **production-ready system** that extracts rich semantic information from images using **advanced multimodal AI techniques**.  

This project enhances user interaction with images and generates **meaningful insights** through **artificial intelligence**.  

---

## 👥 Research & Development Team  

- **Viken Hadavat** – **Team Lead  & ML Engineer**, responsible for project management and architectural design.  
- **Dhruv Singala** – **Lead Developer**, focused on backend development and database management.  
- **Karan Thakkar** – **Software tester & Researcher**, specializing in software testing and research.  

---

## 📊 System Architecture Overview  

The **ImageInsight AI** application is built on a **modular architecture**, consisting of several interconnected components:  

### 1️⃣ Database Migration  
- **Technology Used:** Alembic  
- **Purpose:**  
  - Facilitates **schema changes** in the database for smooth updates and enhancements.  
  - Implements **email verification fields** (`verified` and `verification_token`) to improve user security.  

### 2️⃣ Flask Application  
- **Role:**  
  - Serves as the **backend**, handling user authentication, session management, and image uploads.  
  - Manages API interactions with the **Gemini model** for image analysis.  
- **Key Features:**  
  ✅ User Registration – Secure password hashing & account management.  
  ✅ Login System – Credential validation & session handling.  
  ✅ Image Processing – AI-driven image analysis with real-time insights.  

### 3️⃣ Streamlit Application  
- **Role:**  
  - Provides an **interactive user interface** for image uploads and analysis.  
- **Key Features:**  
  ✅ **File Upload** – Accepts `jpg, jpeg, png` formats.  
  ✅ **Analysis Trigger** – Sends images for AI analysis and displays real-time results.  

### 4️⃣ CSS Styles  
- **Purpose:**  
  - Defines **visual appearance** and ensures a **responsive** user interface.  
- **Key Elements:**  
  ✅ **Responsive Design** – Works across mobile & desktop devices.  
  ✅ **Component Styling** – Enhances UI/UX with styled buttons, modals, and layouts.  

### 5️⃣ JavaScript Functionality  
- **Role:**  
  - Enhances UI interactivity & user experience.  
- **Key Features:**  
  ✅ **Sidebar Toggle** – Expand/collapse navigation menu.  
  ✅ **Modal Dialogs** – Manage login/signup popups.  
  ✅ **File Upload Previews** – Show preview before submission.  

### 6️⃣ Docker Configuration  
- **Purpose:**  
  - Ensures a **consistent, containerized** environment for deployment.  
- **Key Elements:**  
  ✅ **Base Image** – Uses `Python 3.9 slim` for efficiency.  
  ✅ **Dependency Installation** – Installs required packages (`requirements.txt`).  
  ✅ **Port Exposure** – Enables **Streamlit** access on specified ports.  

---

## 🚀 Deployment Instructions  

### System Requirements  
- **Python Version:** `3.7+`  
- **Google API Key:** Required to access **Gemini Pro** AI model.  

### Install Dependencies  
Run the following command:  


# 🚀 AI-Powered Image Analysis with Gemini API  

This project leverages **Google's Gemini AI models** for advanced multimodal image analysis. It enables users to extract **rich semantic insights** from images using state-of-the-art **AI-powered** vision models.  

---

## 🔑 Configure API Authentication  

To use the **Gemini API**, follow these steps to **securely authenticate** your application:  

### 1️⃣ Obtain API Key  
Retrieve your API key from either:  
- **Google AI Studio**  
- **Google Cloud Console**  

### 2️⃣ Enable Generative AI API  
- Set up a project in **Google Cloud Console**  
- Enable the **Generative AI API**  

### 3️⃣ Secure API Key  
To prevent **unauthorized access**, apply the following security measures:  
✅ **Referrer Restrictions** – Limit API key usage to specific domains.  
✅ **IP Whitelisting** – Restrict API calls to trusted IP addresses.  

---

## ⚙️ Technical Competencies  

The project demonstrates expertise in:  

✅ **Multimodal AI** – Understanding AI capabilities & constraints.  
✅ **API Integration Patterns** – Secure methods for AI service connections.  
✅ **Prompt Engineering** – Optimizing prompts for accurate results.  
✅ **Streamlit Development** – Rapid prototyping for interactive UIs.  
✅ **Security Best Practices** – Credential management & secure coding.  

---

## 🚧 Current Limitations & Constraints  

### 📌 Domain-Specific Constraints  
⚠ **Visual Ambiguity** – Struggles with objects that look alike.  
⚠ **Fine-Grained Detail Extraction** – Limited accuracy for tiny intricate details.  
⚠ **Contextual Understanding** – May misinterpret complex scenarios.  

### 📌 Technical Limitations  
⚠ **Output Variability** – Responses may differ for similar inputs.  
⚠ **Image Quality Dependencies** – Poor-quality images reduce accuracy.  
⚠ **Session State Management** – Challenge in maintaining user context over multiple interactions.  

---

## 🙏 Acknowledgements  

We extend our appreciation to:  

💡 **Google’s AI Research Team** – For providing access to the **Gemini API**.  
💡 **Streamlit Development Team** – For their **interactive framework**.  
💡 **Academic Advisors** – For **guidance and technical support**.  

---

## 📚 References & Resources  

📖 [Streamlit Documentation](https://docs.streamlit.io/)  
📖 [Google Generative AI Docs](https://ai.google.dev/)  
📖 [Gemini API Docs](https://ai.google.dev/docs)  
📖 [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/)  
📖 [Flask Docs](https://flask.palletsprojects.com/en/latest/)  

---

🚀 **Stay tuned for future updates!**  
