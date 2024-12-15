document.getElementById("violation-form").addEventListener("submit", (event) => {
    event.preventDefault(); // 通常のフォーム送信を防止

    const formData = new FormData(event.target);

    // 複数選択された違反内容を配列として取得
    const selectedViolations = Array.from(
        document.getElementById("violations").selectedOptions
    ).map((option) => option.value);

    // フォームデータに選択された違反を追加
    formData.delete("violations"); // 既存の"violations"を削除
    selectedViolations.forEach((id) => formData.append("violations", id)); // すべての選択されたIDを追加

    const resultDiv = document.getElementById("result");

    fetch(event.target.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                resultDiv.innerHTML = `<p style="color: red;">エラー: ${data.error}</p>`;
            } else {
                const violationDetails = data.violations
                    .map(
                        (violation, index) =>
                            `<li>${index + 1}. ${violation.name} - 点数: ${violation.points}, 罰金: ¥${violation.fine}, 刑罰: ${violation.punishment}</li>`
                    )
                    .join("");

                resultDiv.innerHTML = `
                    <h3>計算結果</h3>
                    <p>対象者: ${data.age_group}</p>
                    <ul>${violationDetails}</ul>
                    <p>合計罰金: ¥${data.total_fine}</p>
                    <p>合計点数: ${data.total_points}点</p>
                    <p>予想される刑罰: ${data.possible_punishment}</p>
                `;
            }
        })
        .catch((error) => {
            resultDiv.innerHTML = `<p style="color: red;">サーバーエラーが発生しました: ${error.message}</p>`;
        });
});
