// Función para actualizar la lista de personajes
async function updateList() {
    const res = await fetch(`/api/list/${base}`);
    const data = await res.json();
    const listDiv = document.getElementById("list");
    listDiv.innerHTML = "";
    data.forEach(c => {
        const div = document.createElement("div");
        div.innerHTML = `Nombre: ${c.name}, Rareza: ${c.rarity}, Cuenta: ${c.account} 
        <button onclick="deleteCharacter('${c.name}')">Borrar</button>`;
        listDiv.appendChild(div);
    });
}

// Buscar personaje
async function searchCharacter() {
    const name = document.getElementById("searchName").value;
    if (!name) {
        alert("Escribe un nombre");
        return;
    }
    const res = await fetch(`/api/search?base=${base}&name=${name}`);
    const data = await res.json();
    const searchDiv = document.getElementById("searchResult");
    searchDiv.innerHTML = "";
    if (data.exists) {
        searchDiv.innerHTML = `Ya existe: Nombre: ${data.data.name}, Rareza: ${data.data.rarity}, Cuenta: ${data.data.account}`;
    } else {
        searchDiv.innerHTML = `
            No existe. Agregar:
            <br>
            Rareza: <input id="rarity" placeholder="Ej: comun">
            Cuenta: <input id="account" placeholder="Ej: Guardado1">
            <button onclick="addCharacter('${name}')">Agregar</button>
        `;
    }
}

// Agregar personaje
async function addCharacter(name) {
    const rarity = document.getElementById("rarity").value;
    const account = document.getElementById("account").value;
    if (!rarity || !account) {
        alert("Completa todos los campos");
        return;
    }
    await fetch("/api/add", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({base, name, rarity, account})
    });
    updateList();
    document.getElementById("searchResult").innerHTML = "";
}

// Borrar personaje
async function deleteCharacter(name) {
    await fetch("/api/delete", {
        method: "DELETE",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({base, name})
    });
    updateList();
}

// Cargar lista al inicio
updateList();
