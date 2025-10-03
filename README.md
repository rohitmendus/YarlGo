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
- Students access **batch-specific** question banks for targeted practice.  

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

> *(Add your app screenshots here when available — sample layout below)*  

<img width="1600" alt="Dashboard Screenshot" src="https://via.placeholder.com/1600x800.png?text=YarlGo+Dashboard" />  
<img width="1600" alt="Question Bank Screenshot" src="https://via.placeholder.com/1600x800.png?text=YarlGo+Question+Bank" />  
<img width="1600" alt="Reports Screenshot" src="https://via.placeholder.com/1600x800.png?text=YarlGo+Reports" />  

---

## 📄 License  

This project is licensed under the **GPLv3 License**.  
See the [LICENSE](./LICENSE) file for full details.  

---
