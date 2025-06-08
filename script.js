// Fungsi ini akan dipanggil saat halaman web dimuat
async function populateFormOptions() {
    console.log("Mencoba memuat opsi form dari form_options.json...");
    try {
        const response = await fetch('form_options.json');
        if (!response.ok) {
            throw new Error(`Gagal memuat file konfigurasi! Status: ${response.status}`);
        }
        const options = await response.json();
        console.log("Opsi berhasil dimuat:", options);

        // Fungsi helper untuk mengisi elemen <select>
        const fillSelect = (id, values) => {
            const select = document.getElementById(id);
            if (!select) {
                console.error(`Elemen HTML dengan id '${id}' tidak ditemukan.`);
                return;
            }
            select.innerHTML = ''; // Kosongkan pilihan lama
            values.forEach(option => {
                select.innerHTML += `<option value="${option}">${option}</option>`;
            });
        };

        // Panggil fungsi helper untuk setiap dropdown
        fillSelect('gender', options.gender);
        fillSelect('major', options.major);
        fillSelect('domainInterest', options.domainInterest);
        fillSelect('projects', options.projects);
        console.log("Semua dropdown berhasil diisi.");

    } catch (error) {
        console.error("KRITIS: Gagal memuat atau memproses form_options.json:", error);
        alert("KRITIS: Gagal memuat opsi form. Pastikan file 'form_options.json' ada dan coba refresh halaman. Lihat console (F12) untuk detail.");
    }
}

// Fungsi yang dipanggil saat tombol prediksi diklik
async function submitForm() {
    console.log("Tombol prediksi diklik. Memulai proses...");
    const resultDiv = document.getElementById("result");
    
    try {
        // Ambil semua nilai dari form
        const formData = {
            "Name": document.getElementById("name").value,
            "Age": parseInt(document.getElementById("age").value),
            "GPA": parseFloat(document.getElementById("gpa").value),
            "Gender": document.getElementById("gender").value,
            "Major": document.getElementById("major").value,
            "Python": document.getElementById("pythonSkill").value,
            "SQL": document.getElementById("sqlSkill").value,
            "Java": document.getElementById("javaSkill").value,
            "Interested Domain": document.getElementById("domainInterest").value,
            "Projects": document.getElementById("projects").value
        };
        console.log("Data form yang akan dikirim ke server:", formData);

        // Validasi sederhana
        if (!formData.Name || isNaN(formData.Age) || isNaN(formData.GPA)) {
            throw new Error("Nama, Usia, dan IPK harus diisi dengan benar.");
        }

        // Tampilkan pesan loading
        resultDiv.innerHTML = '🧠 Menganalisis profil Anda...';
        resultDiv.className = 'alert alert-info mt-4'; // Ganti class untuk tampilan loading

        // Kirim data ke server Flask
        console.log("Mengirim permintaan ke server di http://127.0.0.1:5000/predict");
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });

        console.log("Respon dari server diterima. Status:", response.status);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Server merespon dengan status error ${response.status}`);
        }

        const result = await response.json();
        const predictions = result.prediction;
        console.log("Prediksi diterima dari server:", predictions);

        // Tampilkan hasil prediksi
        let resultHTML = `
          Halo <strong>${formData.Name}</strong>!<br>
          Berdasarkan profil Anda, berikut adalah 3 rekomendasi karier teratas:
          <ul class="list-group list-group-flush mt-3">
        `;

        predictions.forEach((item, index) => {
            const isFirst = index === 0;
            resultHTML += `
                <li class="list-group-item d-flex justify-content-between align-items-center ${isFirst ? 'list-group-item-success fw-bold' : ''}">
                    <span>${index + 1}. ${item.group}</span>
                    <span class="badge bg-primary rounded-pill">${item.probability}</span>
                </li>
            `;
        });

        resultHTML += '</ul>';
        resultDiv.innerHTML = resultHTML;
        resultDiv.className = 'alert mt-4'; // Hapus kelas alert-info

    } catch (error) {
        console.error('ERROR di dalam fungsi submitForm:', error);
        resultDiv.innerHTML = `<strong>Oops!</strong> Terjadi kesalahan: ${error.message}`;
        resultDiv.className = 'alert alert-danger mt-4';
    }
}
