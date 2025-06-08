import pandas as pd
df = pd.read_csv('cleaned_cs_students.csv')

# Definisikan lagi mapping yang sama persis seperti di skrip v4
career_to_group_map = {
    'Web Developer': 'Web Development', 'Frontend Developer': 'Web Development', 'Backend Developer': 'Web Development', 'Fullstack Developer': 'Web Development',
    'Ai Engineer': 'AI & Data', 'Machine Learning Engineer': 'AI & Data', 'Data Scientist': 'AI & Data', 'Data Analyst': 'AI & Data', 'Business Intelligence': 'AI & Data',
    'Software Engineer': 'Software Engineering', 'Software Developer': 'Software Engineering', 'System Architect': 'Software Engineering',
    'Mobile Developer': 'Mobile Development', 'Android Developer': 'Mobile Development', 'Ios Developer': 'Mobile Development',
    'Cybersecurity Analyst': 'Cybersecurity', 'Security Engineer': 'Cybersecurity',
    'Game Developer': 'Game & Graphics',
    'Cloud Engineer': 'Cloud & Infra', 'Network Engineer': 'Cloud & Infra', 'Devops Engineer': 'Cloud & Infra',
    'Qa Engineer': 'Software Engineering'
}

df['Career_Group'] = df['Future Career'].apply(lambda x: career_to_group_map.get(x, 'Other'))

# Tampilkan pekerjaan apa saja yang masuk ke grup 'Other' dan jumlahnya
print("Isi dari Grup 'Other':")
other_careers = df[df['Career_Group'] == 'Other']['Future Career'].value_counts()
print(other_careers)