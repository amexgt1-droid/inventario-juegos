// Obtenemos la base desde la URL
const base = new URL(window.location.href).pathname.split("/base/")[1];

// ---------------------------------
// Buscar personaje
// ---------------------------------
async function searchCharacter() {
    const name = document.getElementById("searchName").value.trim();

    if (!name) return alert("Escribe un nombre");

    const res = await fetch(`/api/search?base=${base}&name=${name}`);
    const data = await res.json();

    const box = document.getElementById("searchResult");

    if (!data.exists) {
        box.innerHTML = `
            <p>No existe "${name}". ¿Agregar?</p>
            
            <label>Nombre:</label><br>
            <input id="newName" value="${name}">
            <br><br>

            <label>Rareza:</label><br>
            <input id="newRarity" placeholder="Ej: Común, Raro, Oro...">
            <br><br>

            <label>Cuenta:</label><br>
            <input id="newAccount" placeholder="Ej: Cuenta1, Guardado2...">
            <br><br>

            <button onclick="addCharacter()">Agregar</button>
        `;
    } else {
        const c = data.data;
        box.innerHTML = `
            <h3>Encontrado:</h3>
            <p><strong>Nombre:</strong> ${c.name}</p>
            <p><strong>Rareza:</strong> ${c.rarity}</p>
            <p><strong>Cuenta:</strong> ${c.account}</p>

            <button onclick="deleteCharacter('${c.name}')">Borrar</button>
        `;
    }
}

// ---------------------------------
// Agregar personaje
// ---------------------------------
async function addCharacter() {
    const name = document.getElementById("newName").value.trim();
    const rarity = document.getElementById("newRarity").value.trim();
    const account = document.getElementById("newAccount").value.trim();

    if (!name || !rarity || !account) {
        alert("Llena todos los campos.");
        return;
    }

    await fetch("/api/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ base, name, rarity, account })
    });

    alert("Guardado correctamente!");
    loadList();
    document.getElementById("searchResult").innerHTML = "";
}

// ---------------------------------
// Listar personajes
// ---------------------------------
async function loadList() {
    const res = await fetch(`/api/list/${base}`);
    const chars = await res.json();
    let html = "";

    chars.forEach(c => {
        html += `
            <p>
                <strong>${c.name}</strong> | ${c.rarity} | ${c.account}
                <button onclick="deleteCharacter('${c.name}')">Borrar</button>
            </p>
        `;
    });

    document.getElementById("list").innerHTML = html;
}

// ---------------------------------
// Borrar personaje
// ---------------------------------
async function deleteCharacter(name) {
    if (!confirm(`¿Borrar "${name}"?`)) return;

    await fetch("/api/delete", {
        method: "DELETE",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ base, name })
    });

    loadList();
    document.getElementById("searchResult").innerHTML = "";
}

// ---------------------------------
// Cargar lista al abrir la base
// ---------------------------------
if (window.location.pathname.startsWith("/base/")) {
    loadList();
}
