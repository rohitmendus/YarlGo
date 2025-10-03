# 🎓 YarlGo  

## 📖 Description  
**YarlGo** is an academic **test management platform** designed to help students prepare for competitive and high-stakes exams.  

It provides a **structured and easy-to-use environment** with features like:  
- 📚 **Question Bank**  
- 📊 **Performance Reports**  
- 👥 **Role-Based Access** for Students, Faculty, and Admins  

⚙️ **Tech Stack**  
- **Backend**: Django (secure, scalable, and reliable)  
- **Frontend**: HTMX, jQuery, AJAX (dynamic & interactive UI)  

With YarlGo, institutions can seamlessly manage exams, organize subjects, and track student performance—while students benefit from **personalized reports** and an **accessible study space**.  

---

## ✨ Key Features  

YarlGo empowers institutions, faculty, and students with interactive tools for exam preparation.  

<details>
<summary>🔑 Role-Based Access Control</summary>  

- **Admin**: Manage users, batches, and monitor overall platform usage.  
- **Faculty**: Create/manage exams, subjects, and add questions to the question bank.  
- **Students**: Access question banks, attempt practice tests, and view personalized reports.  

</details>  

<details>
<summary>📚 Exam & Subject Management</summary>  

- Faculty can organize exams into categories and subjects into topics.  
- Ensures alignment with institutional curricula.  

</details>  

<details>
<summary>🗂️ Question Bank</summary>  

- Faculty can add questions with support for **images, equations, and tables**.  
- Bulk upload via Excel templates for efficiency.  
- Students access **subject-specific** question banks for targeted practice.  

</details>  

<details>
<summary>📝 Practice Tests</summary>  

- Faculty can conduct tests using the question bank.  
- Students get **instant, performance-based reports** with metrics like:  
  - ⏱️ Average time per question  
  - 📊 Topic-wise analysis  
  - 👥 Batch-wise comparisons  

</details>  

<details>
<summary>📊 Dashboards & Reports</summary>  

- **Admins/Faculty**: Track user activity, subject engagement, and performance trends.  
- **Students**: View personalized reports to identify strengths & weaknesses.  

</details>  

<details>
<summary>📖 Course & Batch Management</summary>  

- Students grouped into batches by exam category.  
- Faculty manage subjects, topics, and organize content accordingly.  

</details>  

<details>
<summary>👤 Profile Management</summary>  

- Each user has a personal profile page to view/update details.  

</details>  

⚡ *Note: Some features are under development and will be expanded in future updates.*  

---

## 🛠️ Components  

YarlGo is built as a **modular Django project**, with separate apps for each functionality:  

- **Accounts App** 🧑‍💼 (user management & roles)  
- **Exams App** 📝 (exam creation & management)  
- **Subjects App** 📚 (subject & topic handling)  
- **Batches App** 👥 (student grouping & batch organization)  
- **Tests App** 🧪 (practice tests & reports)  

---

## ⚙️ Installation  

1. **Clone the repo**:  
   `git clone https://github.com/rohitmendus/YarlGo.git`  

2. **Navigate into the project directory**:  
   `cd YarlGo`  

3. **Setup a virtual environment**:  
   - Linux/Mac: `python -m venv venv && source venv/bin/activate`  
   - Windows: `python -m venv venv && venv\Scripts\activate`  

4. **Install dependencies**:  
   `pip install -r requirements.txt`  

5. **Apply migrations**:  
   `python manage.py makemigrations && python manage.py migrate`  

6. **Load fixtures (initial data)**:  
   Example: `python manage.py loaddata admin_user.json`  

7. **Run the server**:  
   `python manage.py runserver`  

---

## 📸 Screenshots  

<img width="1351" height="606" alt="Capture" src="https://github.com/user-attachments/assets/4f40b909-be12-49df-9066-acc735cf8fd9" />
<img width="1366" height="608" alt="Capture8" src="https://github.com/user-attachments/assets/20889e06-1f9b-4fc4-b44f-c34c1350b4d2" />
<img width="392" height="521" alt="Capture7" src="https://github.com/user-attachments/assets/c251809b-b2bd-4004-9da7-15a7072fc79d" />
<img width="1366" height="610" alt="Capture6" src="https://github.com/user-attachments/assets/b83cc506-b65c-4137-b8c1-65b3fbd1cdfd" />
<img width="1366" height="608" alt="Capture5" src="https://github.com/user-attachments/assets/0a968d2e-5c28-46b3-ad4a-e1f8667fc1cb" />
<img width="1366" height="607" alt="Capture2" src="https://github.com/user-attachments/assets/cb61a522-4839-43bf-8fcb-6f0e3cdabe13" />
<img width="390" height="521" alt="Capture9" src="https://github.com/user-attachments/assets/9daf8082-a8d2-4b64-b487-fce23bc3a1ce" />
<img width="1366" height="609" alt="Capture12" src="https://github.com/user-attachments/assets/bcf3ecf0-7662-4661-8311-123264cec573" />

---

## 📄 License  

This project is licensed under the **GPLv3 License**.  
See the [LICENSE](./LICENSE) file for full details.  

---
