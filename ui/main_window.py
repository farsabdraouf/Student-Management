import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow:
    def __init__(self, service):
        self.service = service
        self.root = tk.Tk()
        self.root.title("نظام إدارة الطلاب")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create frames
        self.input_frame = ttk.Frame(self.root, padding="10")
        self.input_frame.pack(fill=tk.X)
        
        self.table_frame = ttk.Frame(self.root, padding="10")
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Setup input fields
        ttk.Label(self.input_frame, text="الاسم:").grid(row=0, column=0, padx=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5)
        
        ttk.Label(self.input_frame, text="العمر:").grid(row=0, column=2, padx=5)
        self.age_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.age_var).grid(row=0, column=3, padx=5)
        
        ttk.Label(self.input_frame, text="التخصص:").grid(row=0, column=4, padx=5)
        self.major_var = tk.StringVar()
        ttk.Entry(self.input_frame, textvariable=self.major_var).grid(row=0, column=5, padx=5)
        
        # Setup buttons
        ttk.Button(self.input_frame, text="إضافة", 
                  command=self.add_student).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Button(self.input_frame, text="تحديث", 
                  command=self.update_student).grid(row=1, column=2, columnspan=2, pady=10)
        ttk.Button(self.input_frame, text="حذف", 
                  command=self.delete_student).grid(row=1, column=4, columnspan=2, pady=10)
        
        # Setup search
        ttk.Label(self.input_frame, text="بحث:").grid(row=2, column=0, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        ttk.Entry(self.input_frame, textvariable=self.search_var).grid(
            row=2, column=1, columnspan=5, sticky='ew', padx=5)
        
        # Setup treeview
        self.tree = ttk.Treeview(self.table_frame, columns=('id', 'name', 'age', 'major'), 
                                show='headings')
        
        self.tree.heading('id', text='الرقم')
        self.tree.heading('name', text='الاسم')
        self.tree.heading('age', text='العمر')
        self.tree.heading('major', text='التخصص')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Load initial data
        self.refresh_table()
    
    def refresh_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load students
        students = self.service.get_all_students()
        for student in students:
            self.tree.insert('', 'end', values=(
                student.student_id,
                student.name,
                student.age,
                student.major
            ))
    
    def add_student(self):
        name = self.name_var.get()
        age = self.age_var.get()
        major = self.major_var.get()
        
        if self.service.add_student(name, age, major):
            messagebox.showinfo("نجاح", "تمت إضافة الطالب بنجاح")
            self.clear_inputs()
            self.refresh_table()
        else:
            messagebox.showerror("خطأ", "فشل في إضافة الطالب")
    
    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "الرجاء اختيار طالب للتحديث")
            return
        
        student_id = self.tree.item(selected[0])['values'][0]
        name = self.name_var.get()
        age = self.age_var.get()
        major = self.major_var.get()
        
        if self.service.update_student(student_id, name, age, major):
            messagebox.showinfo("نجاح", "تم تحديث بيانات الطالب بنجاح")
            self.clear_inputs()
            self.refresh_table()
        else:
            messagebox.showerror("خطأ", "فشل في تحديث بيانات الطالب")
    
    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "الرجاء اختيار طالب للحذف")
            return
        
        if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف هذا الطالب؟"):
            student_id = self.tree.item(selected[0])['values'][0]
            if self.service.delete_student(student_id):
                messagebox.showinfo("نجاح", "تم حذف الطالب بنجاح")
                self.clear_inputs()
                self.refresh_table()
            else:
                messagebox.showerror("خطأ", "فشل في حذف الطالب")
    
    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.name_var.set(values[1])
            self.age_var.set(values[2])
            self.major_var.set(values[3])
    
    def on_search_change(self, *args):
        search_term = self.search_var.get()
        if search_term:
            students = self.service.search_students(search_term)
        else:
            students = self.service.get_all_students()
        
        # Clear and reload table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for student in students:
            self.tree.insert('', 'end', values=(
                student.student_id,
                student.name,
                student.age,
                student.major
            ))
    
    def clear_inputs(self):
        self.name_var.set('')
        self.age_var.set('')
        self.major_var.set('')
    
    def run(self):
        self.root.mainloop()

