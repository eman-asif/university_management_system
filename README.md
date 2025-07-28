
## **University Management System – Comprehensive Overview**

The **University Management System (UMS)** is a robust, role-based academic information management platform built using **Django and Django REST Framework**. It is designed to streamline the administration of academic operations, including student enrollment, course management, grading, attendance tracking, faculty coordination, and timetable scheduling.

The system provides distinct access and operational boundaries for **three primary user roles**—**Administrators, Faculty Members, and Students**—ensuring that each user can only access and manage data relevant to their responsibilities. The platform supports fine-grained permissions, data security, and user-specific views for enhanced academic workflow management.

---

### 🔑 **Core Features & Modules**

#### 1. **User & Role Management**

* Users are categorized into **three groups**:

  * `Admin`: Users `a1` to `a5`, with full access and control over the entire system.
  * `Faculty`: Users `f1` to `f14`, responsible for teaching, grading, and attendance.
  * `Students`: Users `s1` to `s40`, enrolled in programs and courses.

* Group-based permissions ensure that:

  * Admins have **unrestricted** read/write access.
  * Faculty members can only interact with data **relevant to their teaching assignments**.
  * Students can access **only their own academic records**.

---

#### 2. **Academic Models & Relationships**

* **Department**: Academic units under which programs and faculty are organized.
* **Program**: Degree or diploma offerings under departments.
* **Course**: Taught within programs and assigned to faculty members.
* **Student**: Registered users enrolled in programs and linked to user accounts.
* **Faculty**: Teachers assigned to departments and courses.
* **Enrollment**: Records of students enrolled in specific courses.
* **Withdrawal**: Students can opt out of courses, recording reasons and dates.
* **Grade**: Records of academic performance per course per student.
* **Attendance**: Daily attendance records per course.
* **Timetable**: Weekly schedule of course sessions.

---

### 🔒 **Role-Based Access Customization**

Each ViewSet is customized with `get_queryset()` methods that dynamically filter data based on the authenticated user's group, user ID, or related objects. Some key logic includes:

* **Students** view only:

  * Their **own grades**, **attendance**, **withdrawals**, and **enrollments**.
  * **Courses they are enrolled in**.
  * **Faculty and timetables** of those courses.
* **Faculty** view only:

  * **Students enrolled in their courses**.
  * Their **own taught courses**, **grades**, **attendance**, and **withdrawals**.
  * **Timetables** related to their teaching responsibilities.
* **Admins** have access to all models and data.

---

### ⚙️ **System Automation & SQL Integration**

* Bulk SQL scripts were used to:

  * Insert departments, programs, and courses.
  * Generate timetables for multiple courses.
  * Populate users with usernames (`a1–a5`, `f1–f14`, `s1–s40`) and assign them to their groups.
  * Update models like `Faculty` and `Student` by linking appropriate `user_id`s.
  * Assign permissions, `is_staff`, and `is_superuser` flags accordingly.

---

### 📄 **Security and Permissions**

* Utilizes Django’s **Group**, **Permission**, and **Model-level permissions** via `DjangoModelPermissions`.
* `IsAuthenticated` ensures only logged-in users can access data.
* Login endpoint is protected via standard **DRF authentication mechanisms**.

---

### 📦 **REST API Design**

* Built on **ModelViewSet** using DRF routers.
* Pagination added for better scalability.
* Easy integration with frontend frameworks or mobile applications via REST endpoints.

---

### 📘 **Conclusion**

The system offers a **centralized, secure, and scalable** architecture for managing university operations. By providing **customized views** and access rights for students, faculty, and administrators, the platform ensures data privacy, simplifies academic workflows, and enhances user experience across all levels of university administration.

