document.addEventListener("DOMContentLoaded", () => {
    const tabelaCorpo = document.getElementById("tabela-produtos-corpo");
    const btnAtualizar = document.getElementById("btn-atualizar");
    const cardAlertas = document.getElementById("card-total-alertas");
    const cardTotal = document.getElementById("card-total-produtos");
    // const selectProduto = document.getElementById("select-produto");
    // const formMovimentacao = document.getElementById("form-movimentacao");    
    // const mensagemStatus = document.getElementById("mensagem-status");

    // // Função para exibir alertas dinâmicos
    // function exibirMensagem(texto, tipo = "sucesso") {
    //     if (!mensagemStatus) return;
    //     mensagemStatus.textContent = texto;
    //     mensagemStatus.className = `alerta alerta-${tipo}`;
    //     mensagemStatus.classList.remove("oculto");

    //     setTimeout(() => {
    //         mensagemStatus.classList.add("oculto");
    //     }, 4000);
    // }

    // Carregar a lista de produtos da API REST
    async function carregarProdutos() {
        try {
            const resposta = await fetch("/api/produtos");
            if (!resposta.ok) throw new Error("Falha ao consultar a API.");

            const produtos = await resposta.json();
            renderizarDashboard(produtos);
            preencherSelectProdutos(produtos);
        } catch (erro) {
            tabelaCorpo.innerHTML = `<tr><td colspan="5" class="texto-centro">Erro ao carregar dados do estoque.</td></tr>`;
                        
        }
    }

    // Renderizar linhas da tabela no DOM
    function renderizarDashboard(produtos) {
        // Atualizar contadores dos cards
        const totalAlertas = produtos.filter(p => p.precisa_reposicao).length;
        if (cardAlertas) cardAlertas.textContent = totalAlertas;
        if (cardTotal) cardTotal.textContent = produtos.length;
    
        if (produtos.length === 0) {
            tabelaCorpo.innerHTML = `<tr><td colspan="5" class="texto-centro">Nenhum produto cadastrado no momento.</td></tr>`;
            return;
        }

        // aria-live nos saldos
        tabelaCorpo.innerHTML = produtos.map(prod => {
            const statusBadge = prod.precisa_reposicao
                ? `<span class="badge badge-alerta" role="status" aria-label="Atenção: Saldo abaixo do estoque mínimo. Repor imediatamente.">Abaixo do mínimo</span>`
                : `<span class="badge badge-ok" role="status" aria-label="Estoque normal e adequado">Adequado</span>`;

            return `
                <tr>
                    <td><strong>${prod.sku}</strong></td>
                    <td>${prod.nome}</td>
                    <td id="saldo-${prod.id}" aria-live="polite" aria-atomic="true">${prod.quantidade_atual.toFixed(1)} ${prod.unidade_medida}</td>
                    <td>${prod.estoque_minimo.toFixed(1)} ${prod.unidade_medida}</td>
                    <td>${statusBadge}</td>
                </tr>
            `;
        }).join("");
    }   

    if (btnAtualizar) {
        // aria-label no botão
        btnAtualizar.setAttribute("aria-label", "Atualizar lista e saldos de produtos em tempo real");
        btnAtualizar.addEventListener("click", carregarProdutos);
    }

    // Carga inicial
    carregarProdutos();
});