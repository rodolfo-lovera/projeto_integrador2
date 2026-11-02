document.addEventListener("DOMContentLoaded", () => {
    const tabelaCorpo = document.getElementById("tabela-produtos-corpo");
    const btnAtualizar = document.getElementById("btn-atualizar");
    const cardAlertas = document.getElementById("card-total-alertas");
    const cardTotal = document.getElementById("card-total-produtos");

    async function carregarProdutos() {
        try {
            const resposta = await fetch("/api/produtos");
            if (!resposta.ok) throw new Error("Falha ao consultar a API.");

            const produtos = await resposta.json();
            renderizarDashboard(produtos);
        } catch (erro) {
            console.error("Erro capturado no estoque.js:", erro);
            if (tabelaCorpo) {
                tabelaCorpo.innerHTML = `<tr><td colspan="5" style="text-align: center; color: red;">Erro ao carregar dados do estoque.</td></tr>`;
            }
        }
    }

    function renderizarDashboard(produtos) {
        if (!Array.isArray(produtos)) return;

        // Atualiza contadores dos cards
        const totalAlertas = produtos.filter(p => p.precisa_reposicao).length;
        if (cardAlertas) cardAlertas.textContent = totalAlertas;
        if (cardTotal) cardTotal.textContent = produtos.length;

        if (!tabelaCorpo) return;

        if (produtos.length === 0) {
            tabelaCorpo.innerHTML = `<tr><td colspan="5" style="text-align: center; padding: 1.5rem;">Nenhum produto cadastrado no momento.</td></tr>`;
            return;
        }

        // Renderiza linhas de forma segura contra campos nulos
        tabelaCorpo.innerHTML = produtos.map(prod => {
            const qtdAtual = Number(prod.quantidade_atual ?? 0);
            const qtdMinima = Number(prod.estoque_minimo ?? 0);
            const unidade = prod.unidade_medida || "UN";

            const statusBadge = prod.precisa_reposicao
                ? `<span class="badge badge-alert" role="status" aria-label="Atenção: Abaixo do Mínimo">⚠️ Repor</span>`
                : `<span class="badge badge-ok" role="status" aria-label="Estoque Adequado">✓ Adequado</span>`;

            return `
                <tr>
                    <td><strong>${prod.sku || "-"}</strong></td>
                    <td>${prod.nome || "-"}</td>
                    <td id="saldo-${prod.id}" aria-live="polite">${qtdAtual.toFixed(1)} ${unidade}</td>
                    <td>${qtdMinima.toFixed(1)} ${unidade}</td>
                    <td>${statusBadge}</td>
                </tr>
            `;
        }).join("");
    }

    if (btnAtualizar) {
        btnAtualizar.addEventListener("click", carregarProdutos);
    }

    carregarProdutos();
});