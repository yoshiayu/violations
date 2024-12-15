document.getElementById('violation-form').addEventListener('submit', (event) => {
    event.preventDefault(); // 通常のフォーム送信を防止

    const formData = new FormData(event.target);
    const resultDiv = document.getElementById('result'); // 結果を表示するエリア

    fetch(event.target.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">エラー: ${data.error}</p>`;
        } else {
            // 違反内容をリスト形式で表示
            const violationDetails = data.violations
                .map(
                    (violation) =>
                        `<li>${violation.name} - 点数: ${violation.points}, 罰金: ¥${violation.fine}</li>`
                )
                .join("");

            // 結果を表示
            resultDiv.innerHTML = `
                <h3>計算結果</h3>
                <p>対象者: ${data.age_group === "adult" ? "成人" : "未成年"}</p>
                <ul>${violationDetails}</ul>
                <p>合計罰金: ¥${data.total_fine}</p>
                <p>合計点数: ${data.total_points}点</p>
            `;
        }
    })
    .catch((error) => {
        resultDiv.innerHTML = `<p style="color: red;">サーバーエラーが発生しました: ${error.message}</p>`;
    });
});
