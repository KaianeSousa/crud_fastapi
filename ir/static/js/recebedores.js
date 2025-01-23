const apiUrl = "/recebedores";

document.addEventListener("DOMContentLoaded", () => {
    const btnVoltar = document.getElementById("btnVoltar");
    const btnCadastrar = document.getElementById("btnCadastrar");
    const btnCancelar = document.getElementById("btnCancelar");
    const form = document.getElementById("form");
    const tabelaRecebedores = document.querySelector(".tabela-recebedores-body");


    async function carregarRecebedores() {
        try {
            const response = await fetch(`${apiUrl}/listar`);
            if (response.ok) {
                const recebedores = await response.json();
                console.log(recebedores);
                tabelaRecebedores.innerHTML = "";
                recebedores.forEach(recebedor => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${recebedor.nome}</td>
                        <td>${recebedor.idade}</td>
                        <td>${recebedor.tipo_sanguineo}</td>
                        <td>${recebedor.necessidades_de_sangue}</td>
                        <td>
                            <button class="btnEditar" data-id="${recebedor.id}" type="button">Editar</button>
                            <button class="btnDeletar" data-id="${recebedor.id}" type="button">Deletar</button>
                        </td>
                    `;
                    tabelaRecebedores.appendChild(row);
                });
            }
        } catch (e) {
            alert("Erro ao carregar recebedores: " + e.message);
        }
    }


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
            tipo_sanguineo: formData.get("tipoSanguineo"),
            necessidades_de_sangue: formData.get("motivoDoacao"),
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
                await carregarRecebedores()
                form.reset();
            } else {
                const error = await response.json();
                alert("Erro ao adicionar recebedor: " + error.detail);
            }
        } catch (e) {
            alert("Não foi possível adicionar ao banco: " + e.message);
        }
    });
    carregarRecebedores()
});
