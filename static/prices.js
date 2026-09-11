function cell(text, className) {
    const td = document.createElement("td");
    td.textContent = text;
    if (className) {
        td.className = className;
    }
    return td;
}

function textOrDash(value) {
    return value ?? "—";
}

function fillRow(tr, coin) {
    const cells = tr.querySelectorAll("td");
    if (cells.length !== 4) {
        tr.replaceChildren(
            cell(coin.symbol),
            cell(coin.coingecko_id),
            cell(textOrDash(coin.price), "price"),
            cell(textOrDash(coin.updated_at)),
        );
        return;
    }
    cells[0].textContent = coin.symbol;
    cells[1].textContent = coin.coingecko_id;
    cells[2].textContent = textOrDash(coin.price);
    cells[2].className = "price";
    cells[3].textContent = textOrDash(coin.updated_at);
}

function renderCoins(coins) {
    const tbody = document.getElementById("coins-body");
    if (!tbody) {
        return;
    }

    if (!coins.length) {
        tbody.replaceChildren();
        const tr = document.createElement("tr");
        const td = document.createElement("td");
        td.colSpan = 4;
        td.textContent = "No coins yet";
        tr.appendChild(td);
        tbody.appendChild(tr);
        return;
    }

    const rows = [...tbody.querySelectorAll("tr")];
    if (rows.length === 1 && rows[0].querySelector("td[colspan]")) {
        rows[0].remove();
        rows.length = 0;
    }

    coins.forEach((coin, i) => {
        let tr = rows[i];
        if (!tr) {
            tr = document.createElement("tr");
            tbody.appendChild(tr);
        }
        fillRow(tr, coin);
    });

    for (let i = coins.length; i < rows.length; i++) {
        rows[i].remove();
    }
}

async function refreshPrices() {
    try {
        const response = await fetch("/api/prices");
        if (!response.ok) {
            return;
        }
        const data = await response.json();
        renderCoins(data.coins);
    } catch (error) {
        console.error("Failed to refresh prices", error);
    }
}

setInterval(refreshPrices, 60000);
