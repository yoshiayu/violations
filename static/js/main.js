document.getElementById("age-group").addEventListener("change", (event) => {
    const ageGroup = event.target.value;
    updateViolations(ageGroup); 
});

// 違反リストを更新する関数
function updateViolations(ageGroup) {
    fetch(`/get_violations/?age_group=${ageGroup}`)
        .then((response) => response.json())
        .then((data) => {
            const violationSelections = document.querySelectorAll("select[name='violations']");
            violationSelections.forEach((select) => {
                select.innerHTML = ""; // セレクトボックスをリセット

                // "選択なし"を追加
                const defaultOption = document.createElement("option");
                defaultOption.value = "32"; // データベースの"選択なし"のID
                defaultOption.textContent = "選択なし";
                select.appendChild(defaultOption);

                // 他の違反内容を追加
                data.forEach((violation) => {
                    const option = document.createElement("option");
                    option.value = violation.id;
                    option.textContent = violation.name;
                    select.appendChild(option);
                });

                // デフォルトで"選択なし"を選択
                select.value = "32";
            });
        })
        .catch((error) => {
            console.error("違反リストの更新に失敗しました:", error);
        });
}

// ページ読み込み時に初期化
document.addEventListener("DOMContentLoaded", () => {
    updateViolations("adult"); // デフォルトで成人のリストをロード
});


document.addEventListener("DOMContentLoaded", () => {
    const selects = document.querySelectorAll("select[name='violations']");
    selects.forEach(select => {
        if (!select.value) {
            select.value = "32"; // ID 31 の「選択なし」をデフォルトに設定
        }
    });
});

document.getElementById("violation-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);

    try {
        const response = await fetch(event.target.action, {
            method: "POST",
            body: formData,
            headers: { "X-CSRFToken": formData.get("csrfmiddlewaretoken") },
        });
        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            const details = data.violations.map((v) =>
                `<li>${v.name}: 点数 ${v.points}, 罰金 ¥${v.fine}, 懲役/禁錮 ${v.punishment}</li>`
            ).join("");

            document.getElementById("result").innerHTML = `
                <h3>計算結果</h3>
                <p>対象者: ${data.age_group}</p>
                <ul>${details}</ul>
                <p>合計点数: ${data.total_points}</p>
                <p>合計罰金: ¥${data.total_fine}</p>
                <p>最も重い罰: ${data.possible_punishment}</p>
                <p>免許状態: ${data.license_status}</p>
            `;
        }
    } catch (error) {
        console.error("エラー:", error);
        document.getElementById("result").innerHTML = `<p style="color: red;">サーバーエラーが発生しました。</p>`;
    }
});

// 初期表示時の違反リスト更新
updateViolations("adult");
