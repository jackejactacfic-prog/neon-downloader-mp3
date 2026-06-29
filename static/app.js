async function baixar(format) {
    const url = document.getElementById("url").value;
    const status = document.getElementById("status");

    status.innerHTML = `Processando ${format.toUpperCase()}... ⏳`;

    const res = await fetch("/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ url, format })
    });

    const data = await res.json();

    if (data.ok) {
        status.innerHTML = `Download concluído! ✔ (${format.toUpperCase()})`;
    } else {
        status.innerHTML = "Erro: " + data.error;
    }
}