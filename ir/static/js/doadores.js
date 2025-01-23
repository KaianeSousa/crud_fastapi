const apiUrl = "/doadores";

document.addEventListener("DOMContentLoaded", () => {
    const btnVoltar = document.getElementById("btnVoltar");
    const btnCadastrar = document.getElementById("btnCadastrar");
    const btnCancelar = document.getElementById("btnCancelar");
    const form = document.getElementById("form");
    const nome = document.getElementById("nome");
    const idade = document.getElementById("idade");
    const tipoSanguineo = document.getElementById("tipoSanguineo");
    const ultimaDoacao = document.getElementById("ultimaDoacao");
    const tabelaDoadores = document.querySelector(".tabela-doadores tbody");

    async function carregarDoadores() {
        try {
            const response = await fetch(`${apiUrl}/listar`);
            if (response.ok) {
                const doadores = await response.json();
                tabelaDoadores.innerHTML = "";
                doadores.forEach(doador => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${doador.nome}</td>
                        <td>${doador.idade}</td>
                        <td>${doador.tipo_sanguineo}</td>
                        <td>${doador.data_da_ultima_doacao}</td>
                        <td>
                            <button class="btnEditar" data-id="${doador.id}" type="button">Editar</button>
                            <button class="btnDeletar" data-id="${doador.id}" type="button">Deletar</button>
                        </td>
                    `;
                    tabelaDoadores.appendChild(row);
                });
                adicionarEventosBotoes();
            }
        } catch (e) {
            alert("Erro ao carregar doadores: " + e.message);
        }
    }

    function adicionarEventosBotoes() {
        document.querySelectorAll(".btnEditar").forEach(botao => {
            botao.addEventListener("click", async (e) => {
                const id = e.target.getAttribute("data-id");
                try {
                    const response = await fetch(`${apiUrl}/buscar/${id}`);
                    if (response.ok) {
                        const doador = await response.json();
                        nome.value = doador.nome;
                        idade.value = doador.idade;
                        tipoSanguineo.value = doador.tipo_sanguineo;
                        ultimaDoacao.value = doador.data_da_ultima_doacao;
                        document.getElementById("form-title").textContent = "Editar Doador";
                        form.style.display = "block";
                        form.onsubmit = async (e) => {
                            e.preventDefault();
                            const data = {
                                nome: nome.value,
                                idade: parseInt(idade.value),
                                tipo_sanguineo: tipoSanguineo.value,
                                data_da_ultima_doacao: ultimaDoacao.value
                            };
                            try {
                                const response = await fetch(`${apiUrl}/atualizar/${id}`, {
                                    method: "PUT",
                                    headers: {
                                        "Content-Type": "application/json",
                                    },
                                    body: JSON.stringify(data),
                                });
                                if (response.ok) {
                                    alert("Doador atualizado com sucesso!");
                                    form.reset();
                                    form.style.display = "none";
                                    carregarDoadores();
                                } else {
                                    const error = await response.json();
                                    alert("Erro ao atualizar doador: " + JSON.stringify(error));
                                }
                            } catch (e) {
                                alert("Erro ao atualizar: " + e.message);
                            }
                        };
                    }
                } catch (e) {
                    alert("Erro ao carregar doador para edição: " + e.message);
                }
            });
        });

        document.querySelectorAll(".btnDeletar").forEach(botao => {
            botao.addEventListener("click", async (e) => {
                const id = e.target.getAttribute("data-id");
                if (confirm("Tem certeza que deseja deletar este doador?")) {
                    try {
                        const response = await fetch(`${apiUrl}/deletar/${id}`, {
                            method: "DELETE",
                        });
                        if (response.ok) {
                            alert("Doador deletado com sucesso!");
                            carregarDoadores();
                        } else {
                            alert("Erro ao deletar doador");
                        }
                    } catch (e) {
                        alert("Erro ao deletar: " + e.message);
                    }
                }
            });
        });
    }

    btnCadastrar.addEventListener("click", () => {
        form.reset();
        document.getElementById("form-title").textContent = "Adicionar Doador";
        form.style.display = "block";
        form.onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                nome: nome.value,
                idade: parseInt(idade.value),
                tipo_sanguineo: tipoSanguineo.value,
                data_da_ultima_doacao: ultimaDoacao.value
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
                    alert("Doador adicionado com sucesso!");
                    form.reset();
                    form.style.display = "none";
                    carregarDoadores();
                } else {
                    const error = await response.json();
                    alert("Erro ao adicionar doador: " + JSON.stringify(error));
                }
            } catch (e) {
                alert("Não foi possível adicionar ao banco: " + e.message);
            }
        };
    });

    btnCancelar.addEventListener("click", () => {
        form.style.display = "none";
    });

    carregarDoadores();
});
