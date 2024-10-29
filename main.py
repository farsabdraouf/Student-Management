from repositories.student_repository import StudentRepository
from services.student_service import StudentService
from ui.main_window import MainWindow

def main():
    repository = StudentRepository()
    service = StudentService(repository)
    app = MainWindow(service)
    app.run()

if __name__ == "__main__":
    main()
