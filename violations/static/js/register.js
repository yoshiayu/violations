document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const usernameInput = document.getElementById("username");
    const password1Input = document.getElementById("password1");
    const password2Input = document.getElementById("password2");

    form.addEventListener("submit", (e) => {
        let isValid = true;

        // ユーザー名のバリデーション
        if (!usernameInput.value.trim()) {
            document.getElementById("username-error").style.display = "block";
            isValid = false;
        } else {
            document.getElementById("username-error").style.display = "none";
        }

        // パスワードのバリデーション
        if (password1Input.value.length < 8 || /^\d+$/.test(password1Input.value)) {
            document.getElementById("password1-error").style.display = "block";
            isValid = false;
        } else {
            document.getElementById("password1-error").style.display = "none";
        }

        // 確認用パスワードのバリデーション
        if (password1Input.value !== password2Input.value) {
            document.getElementById("password2-error").style.display = "block";
            isValid = false;
        } else {
            document.getElementById("password2-error").style.display = "none";
        }

        if (!isValid) e.preventDefault();
    });
});
