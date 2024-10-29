// المتغيرات العامة
let students = [];
const API_URL = 'http://localhost:5000/api';

// دوال مساعدة للتصدير
function exportToCSV() {
    if (students.length === 0) {
        alert('لا توجد بيانات للتصدير');
        return;
    }

    const headers = ['الاسم', 'العمر', 'التخصص'];
    const csvContent = [
        headers.join(','),
        ...students.map(student => 
            [student.name, student.age, student.major].join(',')
        )
    ].join('\n');

    downloadFile(csvContent, 'students.csv', 'text/csv');
}

function exportToJSON() {
    if (students.length === 0) {
        alert('لا توجد بيانات للتصدير');
        return;
    }
    
    const jsonContent = JSON.stringify(students, null, 2);
    downloadFile(jsonContent, 'students.json', 'application/json');
}

function exportToExcel() {
    if (students.length === 0) {
        alert('لا توجد بيانات للتصدير');
        return;
    }

    // إنشاء جدول يمكن فتحه في Excel
    const headers = ['الاسم', 'العمر', 'التخصص'];
    const excelContent = `
        <table>
            <tr>${headers.map(header => `<th>${header}</th>`).join('')}</tr>
            ${students.map(student => `
                <tr>
                    <td>${student.name}</td>
                    <td>${student.age}</td>
                    <td>${student.major}</td>
                </tr>
            `).join('')}
        </table>
    `;

    // تنسيق Excel
    const excelFile = `
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    table { border-collapse: collapse; }
                    th, td { border: 1px solid black; padding: 5px; }
                </style>
            </head>
            <body>
                ${excelContent}
            </body>
        </html>
    `;

    downloadFile(excelFile, 'students.xls', 'application/vnd.ms-excel');
}

function downloadFile(content, fileName, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const downloadLink = document.createElement('a');
    downloadLink.href = url;
    downloadLink.download = fileName;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    window.URL.revokeObjectURL(url);
}

// تحسين دوال النافذة المنبثقة
function showModal() {
    const modal = document.getElementById('studentModal');
    modal.classList.remove('opacity-0', 'pointer-events-none');
    document.body.classList.add('modal-active');
}

function closeModal() {
    const modal = document.getElementById('studentModal');
    modal.classList.add('opacity-0', 'pointer-events-none');
    document.body.classList.remove('modal-active');
    resetForm();
}

function resetForm() {
    const form = document.getElementById('studentForm');
    form.reset();
    document.getElementById('studentId').value = '';
    document.getElementById('modalTitle').textContent = 'إضافة طالب جديد';
}

function openAddModal() {
    resetForm();
    showModal();
}

function openEditModal(student) {
    // تحسين طريقة فتح نافذة التعديل
    document.getElementById('modalTitle').textContent = 'تعديل بيانات الطالب';
    document.getElementById('studentId').value = student.id;
    document.getElementById('nameInput').value = student.name;
    document.getElementById('ageInput').value = student.age;
    document.getElementById('majorInput').value = student.major;
    showModal();
}

// تحسين التعامل مع API
async function fetchStudents(searchTerm = '') {
    try {
        const url = searchTerm 
            ? `${API_URL}/students?search=${encodeURIComponent(searchTerm)}`
            : `${API_URL}/students`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('فشل في جلب البيانات');
        
        students = await response.json();
        renderStudentsTable();
        fetchStatistics();
    } catch (error) {
        console.error('Error fetching students:', error);
        showError('حدث خطأ أثناء جلب بيانات الطلاب');
    }
}

async function fetchStatistics() {
    try {
        const response = await fetch(`${API_URL}/statistics`);
        if (!response.ok) throw new Error('فشل في جلب الإحصائيات');
        
        const stats = await response.json();
        updateStatistics(stats);
    } catch (error) {
        console.error('Error fetching statistics:', error);
        showError('حدث خطأ أثناء جلب الإحصائيات');
    }
}

async function saveStudent(data) {
    try {
        const url = data.id 
            ? `${API_URL}/students/${data.id}`
            : `${API_URL}/students`;
        
        console.log("Sending data:", data); // هنا يتم إضافة `console.log`
        
        const response = await fetch(url, {
            method: data.id ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'حدث خطأ أثناء حفظ البيانات');
        }

        closeModal();
        await fetchStudents();
        showSuccess(data.id ? 'تم تحديث البيانات بنجاح' : 'تم إضافة الطالب بنجاح');
    } catch (error) {
        console.error('Error saving student:', error);
        showError(error.message);
    }
}


async function deleteStudent(id) {
    if (!confirm('هل أنت متأكد من حذف هذا الطالب؟')) return;

    try {
        const response = await fetch(`${API_URL}/students/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'حدث خطأ أثناء حذف الطالب');
        }

        await fetchStudents();
        showSuccess('تم حذف الطالب بنجاح');
    } catch (error) {
        console.error('Error deleting student:', error);
        showError(error.message);
    }
}

// تحسين عرض البيانات
function renderStudentsTable() {
    const tbody = document.getElementById('studentsTableBody');
    tbody.innerHTML = '';

    if (students.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-4 text-gray-500">
                    لا توجد بيانات للعرض
                </td>
            </tr>
        `;
        return;
    }

    students.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">${escapeHtml(student.name)}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${student.age}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">${escapeHtml(student.major)}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-left text-sm font-medium">
                <button onclick='openEditModal(${JSON.stringify(student)})' 
                        class="text-blue-600 hover:text-blue-900 ml-3">
                    <i class="fas fa-edit"></i> تعديل
                </button>
                <button onclick="deleteStudent(${student.id})" 
                        class="text-red-600 hover:text-red-900">
                    <i class="fas fa-trash"></i> حذف
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateStatistics(stats) {
    document.getElementById('totalStudents').textContent = stats.total_students;
    document.getElementById('avgAge').textContent = stats.average_age.toFixed(1);
    document.getElementById('majorCount').textContent = Object.keys(stats.students_by_major).length;
}

// دوال المساعدة الإضافية
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function showError(message) {
    alert(message); // يمكن تحسينها لاستخدام مكتبة toast
}

function showSuccess(message) {
    alert(message); // يمكن تحسينها لاستخدام مكتبة toast
}

// إعداد الأحداث
document.addEventListener('DOMContentLoaded', () => {
    // نموذج إضافة/تعديل الطالب
    document.getElementById('studentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            name: document.getElementById('nameInput').value.trim(),
            age: parseInt(document.getElementById('ageInput').value),
            major: document.getElementById('majorInput').value.trim()
        };

        // التحقق من صحة البيانات
        if (!data.name || !data.age || !data.major) {
            showError('جميع الحقول مطلوبة');
            return;
        }

        if (data.age < 16 || data.age > 100) {
            showError('العمر يجب أن يكون بين 16 و 100');
            return;
        }
        
        const studentId = document.getElementById('studentId').value;
        if (studentId) {
            data.id = parseInt(studentId);
        }
        
        await saveStudent(data);
    });

    // البحث
    const searchInput = document.getElementById('searchInput');
    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            fetchStudents(e.target.value.trim());
        }, 300);
    });

    // أزرار التصدير
    document.getElementById('exportCSV').addEventListener('click', exportToCSV);
    document.getElementById('exportJSON').addEventListener('click', exportToJSON);
    document.getElementById('exportExcel').addEventListener('click', exportToExcel);

    // تحميل البيانات الأولية
    fetchStudents();
});