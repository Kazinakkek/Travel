document.addEventListener('DOMContentLoaded', function () {
    // Ёффекты дл€ кнопки отправки
    const submitBtn = document.getElementById('submitBtn');

    if (submitBtn) {
        submitBtn.addEventListener('mouseover', function () {
            this.style.color = '#ffffff';
            this.style.backgroundColor = '#1565c0';
        });

        submitBtn.addEventListener('mouseout', function () {
            this.style.color = '';
            this.style.backgroundColor = '';
        });
    }

    // Ёффекты дл€ полей ввода
    const inputFields = document.querySelectorAll('input[type="text"], input[type="email"], textarea, select');

    inputFields.forEach(field => {
        field.addEventListener('focus', function () {
            this.style.backgroundColor = '#f0f8ff';
            this.style.borderColor = '#1e88e5';
        });

        field.addEventListener('blur', function () {
            this.style.backgroundColor = '';
            this.style.borderColor = '';
        });
    });
});