import os
import django
from django.db import connection, reset_queries

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course

def run_demo():
    print("\n" + "="*50)
    print("🚀 DEMO QUERY OPTIMIZATION DJANGO ORM")
    print("="*50)
    
    # --- 1. N+1 PROBLEM (BAD PRACTICE) ---
    reset_queries()
    print("\n[1] Menjalankan Query Biasa (N+1 Problem)...")
    courses_bad = list(Course.objects.all())
    for course in courses_bad:
        # Akan memicu query baru ke DB setiap kali memanggil FK
        print(f" - {course.title} by {course.instructor.username} (Kategori: {course.category.name})")
    
    queries_bad = len(connection.queries)
    print(f"❌ JUMLAH QUERY KE DATABASE: {queries_bad}")

    # --- 2. OPTIMIZED (GOOD PRACTICE) ---
    reset_queries()
    print("\n[2] Menjalankan Query Teroptimasi (select_related & prefetch_related)...")
    courses_good = list(Course.objects.for_listing())
    for course in courses_good:
        print(f" - {course.title} by {course.instructor.username} (Kategori: {course.category.name})")
    
    queries_good = len(connection.queries)
    print(f"✅ JUMLAH QUERY KE DATABASE: {queries_good}")
    
    print("\n" + "="*50)
    print(f"KESIMPULAN: Optimasi menghemat {queries_bad - queries_good} query ke database!")
    print("="*50 + "\n")

if __name__ == '__main__':
    run_demo()