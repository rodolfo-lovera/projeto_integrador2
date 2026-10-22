document.addEventListener("DOMContentLoaded", () => {
    const tabelaCorpo = document.getElementById("tabela-produtos-corpo");
    const selectProduto = document.getElementById("select-produto");
    const formMovimentacao = document.getElementById("form-movimentacao");
    const btnAtualizar = document.getElementById("btn-atualizar");
    const mensagemStatus = document.getElementById("mensagem-status");

    // Função para exibir alertas dinâmicos
    function exibirMensagem(texto, tipo = "sucesso") {
        if (!mensagemStatus) return;
        mensagemStatus.textContent = texto;
        mensagemStatus.className = `alerta alerta-${tipo}`;
        mensagemStatus.classList.remove("oculto");

        setTimeout(() => {
            mensagemStatus.classList.add("oculto");
        }, 4000);
    }

    // Carregar a lista de produtos da API REST
    async function carregarProdutos() {
        try {
            const resposta = await fetch("/api/produtos");
            if (!resposta.ok) throw new Error("Falha ao consultar a API.");

            const produtos = await resposta.json();
            renderizarTabela(produtos);
            preencherSelectProdutos(produtos);
        } catch (erro) {
            console.error("Falha ao carregar produtos:", erro);
            if (tabelaCorpo) {
                tabelaCorpo.innerHTML = `<tr><td colspan="5" class="texto-centro">Erro ao carregar dados do estoque.</td></tr>`;
            }
            exibirMensagem("Não foi possível conectar ao servidor.", "erro");
        }
    }

    // Renderizar linhas da tabela no DOM
    function renderizarTabela(produtos) {
        if (!tabelaCorpo) return;

        if (produtos.length === 0) {
            tabelaCorpo.innerHTML = `<tr><td colspan="5" class="texto-centro">Nenhum produto cadastrado no momento.</td></tr>`;
            return;
        }

        tabelaCorpo.innerHTML = produtos.map(prod => {
            const statusBadge = prod.precisa_reposicao
                ? `<span class="badge badge-alerta" role="status">Repor Estoque</span>`
                : `<span class="badge badge-normal" role="status">Adequado</span>`;

            return `
                <tr>
                    <td><strong>${prod.sku}</strong></td>
                    <td>${prod.nome}</td>
                    <td id="saldo-${prod.id}">${prod.quantidade_atual.toFixed(1)} ${prod.unidade_medida}</td>
                    <td>${prod.estoque_minimo.toFixed(1)} ${prod.unidade_medida}</td>
                    <td>${statusBadge}</td>
                </tr>
            `;
        }).join("");
    }

    // Preencher as opções do dropdown do formulário
    function preencherSelectProdutos(produtos) {
        if (!selectProduto) return;
        const valorSelecionadoAnterior = selectProduto.value;
        selectProduto.innerHTML = '<option value="">Selecione um produto...</option>';
        produtos.forEach(prod => {
            const option = document.createElement("option");
            option.value = prod.id;
            option.textContent = `${prod.sku} - ${prod.nome}`;
            selectProduto.appendChild(option);
        });
        if (valorSelecionadoAnterior) {
            selectProduto.value = valorSelecionadoAnterior;
        }
    }

    // Submissão assíncrona do formulário com validação client-side
    if (formMovimentacao) {
        formMovimentacao.addEventListener("submit", async (evento) => {
            evento.preventDefault();

            const produtoId = selectProduto ? selectProduto.value : "";
            const selectTipo = document.getElementById("select-tipo");
            const tipo = selectTipo ? selectTipo.value.toUpperCase() : "ENTRADA";
            const inputQtd = document.getElementById("input-quantidade");
            const inputMotivo = document.getElementById("input-motivo");

            const quantidade = parseFloat(inputQtd ? inputQtd.value : 0);
            const motivo = inputMotivo ? inputMotivo.value.trim() : "";

            // Validações no cliente
            if (!produtoId) {
                exibirMensagem("Selecione um produto.", "erro");
                return;
            }
            if (isNaN(quantidade) || quantidade <= 0) {
                exibirMensagem("Informe uma quantidade válida superior a zero.", "erro");
                return;
            }

            const payload = {
                produto_id: parseInt(produtoId),
                tipo: tipo,
                quantidade: quantidade,
                motivo: motivo
            };

            try {
                const resposta = await fetch("/api/movimentacoes", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });

                // Tratamento defensivo: lê texto puro primeiro
                const textoResposta = await resposta.text();
                let resultado = {};

                try {
                    resultado = JSON.parse(textoResposta);
                } catch (e) {
                    // Se a resposta for HTML (ex: página 404 do Flask)
                    throw new Error(`Servidor retornou erro HTTP ${resposta.status} (${resposta.statusText})`);
                }

                if (!resposta.ok) {
                    throw new Error(resultado.erro || "Erro ao registrar movimentação.");
                }

                exibirMensagem(resultado.mensagem, "sucesso");
                formMovimentacao.reset();
                carregarProdutos(); // Atualiza a tabela dinamicamente
            } catch (erro) {
                console.error("Erro na requisição:", erro);
                exibirMensagem(erro.message, "erro");
            }

            //    try {
            //         const resposta = await fetch("/api/movimentacoes", {
            //             method: "POST",
            //             headers: { "Content-Type": "application/json" },
            //             body: JSON.stringify(payload)
            //         });

            //         const resultado = await resposta.json();

            //         if (!resposta.ok) {
            //             throw new Error(resultado.erro || "Erro ao registrar movimentação.");
            //         }

            //         exibirMensagem(resultado.mensagem, "sucesso");
            //         formMovimentacao.reset();
            //         carregarProdutos(); // Atualiza os dados na tela em segundo plano
            //     } catch (erro) {
            //         console.error("Erro na requisição:", erro);
            //         exibirMensagem(erro.message, "erro");
            //     }
        });
    }

    if (btnAtualizar) {
        btnAtualizar.addEventListener("click", carregarProdutos);
    }

    // Carga inicial
    carregarProdutos();
});