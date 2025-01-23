const apiUrl = "/recebedores";

document.addEventListener("DOMContentLoaded", () => {
    const btnVoltar = document.getElementById("btnVoltar");
    const btnCadastrar = document.getElementById("btnCadastrar");
    const btnCancelar = document.getElementById("btnCancelar");
    const form = document.getElementById("form");
    const nome = document.getElementById("nome");
    const idade = document.getElementById("idade");
    const tipoSanguineo = document.getElementById("tipoSanguineo");
    const motivoDoacao = document.getElementById("motivoDoacao");

    btnCadastrar.addEventListener("click", () => {
        form.reset();
        document.getElementById("form-title").textContent = "Adicionar recebedor";
        form.style.display = "block";
    });

    btnCancelar.addEventListener("click", () => {
        form.style.display = "none";
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = {
            nome: formData.get("nome"),
            idade: formData.get("idade"),
            tipoSanguineo: formData.get("tipoSanguineo"),
            motivoDoacao: formData.get("motivoDoacao"),
        };

        try {
            const response = await fetch(`${apiUrl}/adicionar`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Recebedor adicionado com sucesso!");
                form.reset();
            } else {
                const error = await response.json();
                alert("Erro ao adicionar recebedor: " + error.detail);
            }
        } catch (e) {
            alert("Não foi possível adicionar ao banco: " + e.message);
        }
    });
});
