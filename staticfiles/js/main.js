document.getElementById('violation-form').addEventListener('submit', function (event) {
    const ageGroup = document.getElementById('age-group').value;
    const violations = document.getElementById('violations').selectedOptions;

    if (!ageGroup) {
        alert('対象者を選択してください。');
        event.preventDefault();
    }

    if (violations.length === 0) {
        alert('少なくとも1つの違反内容を選択してください。');
        event.preventDefault();
    }
});
