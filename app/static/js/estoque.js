document.addEventListener("DOMContentLoaded",() =>{
    const tabelaCorpo = document.getElementById("tabela-produtos-corpo");
    const selectProduto = document.getElementById("select-produto");
    const formMovimentacao = document.getElementById("form-movimentacao");
    const btnAtualizar = document.getElementById("btn-atualizar");
    const mensagemStatus = document.getElementById("mensagem-status");

    // Função para exibir alertas dinâmicos
    function exibirMensagem(texto, tipo = "sucesso"){
        mensagemStatus.textContent = texto;
        mensagemStatus.className = `alerta alerta-${tipo}`;
        mensagemStatus.classList.remove("oculto");

        setTimeout(() => {
            mensagemStatus. classList.add("oculto");
        },4000);
    }

    // Carregar a lista de produtos da APi Rest
    async function carregarProdutos(){
        try{
            const resposta = await fetch("/api/produtos");
            if(!resposta.ok) throw new Error("Falha ao consultar a API.");

            const produtos = await resposta.json();
            renderizarTabela(produtos);
            preencherSelectProdutos(produtos);
        } catch (erro) {
            tabelaCorpo.innerHTML = `<tr><td colspan="5" class="texto-centro">Erro ao carregar dados do estoque</td></tr>`;
            exibirMensagem("Não foi possível conectar ao servidor.", "erro");            
        }
    }

    // Renderizar linhas da tabela do DOM
    function renderizarTabela(produtos){
        if (produtos.lenght === 0) {
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
                        <td>{statusBadge}</td>
                    </tr>
                `;
        }).join("");
    }

    // Preencher as opções do dropdown do formulário
    function preencherSelectProdutos(produtos){
        selectProduto.innerHTML = '<option value="">Selecione um produto...</option>';
        produtos.forEach(prod => {
            const option = document.createElement("option");
            option.value = prod.id;
            option.textContent = `${prod.sku} - ${prod.nome}`;
            selectProduto.appendChild(option);
        })
    }

    // Submissão assíncrona do formulário com validação client-side
    formMovimentacao.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        const produtoId = selesctProduto.value;
        const tipo = document. getElementById("select-tipo").value;
        const quantidade = parseFloat(document.getElementById("input=quantidade").value);
        const motivo = document.getElementById("input-motivo").value.trim();

        // Validação no cliente
        if (!produtoId){
            exibirMensagem("Selecione um produto.", "erro");
            return;
        }
        if (isNaN(quantidade) || quantidade <=0){
            exibirMensagem("Informe uma quantidade válida superior a zero.", "erro");
            return;
        }

        const payload = {
            produto_id: parseInt(produtoId),
            tipo: tipo,
            quantidade: quantidade,
            motivo: DeviceMotionEvent
        };

        try {
            const resposta = await fetch("/api/movimentacoes", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const resultado = await resposta.json();

            if (!resposta.ok) {
                throw new Error(resultado.erro || "Erro ao registrar movimentação.");
            }

            exibirMensagem(resultado.mensagem, "sucesso");
            formMovimentacao.reset();

            // recarrega a tabela assincronamente refletindo os novos saldos
            carregarProdutos();
        } catch (erro) {
            exibirMensagem(erro.messagem, "erro");
        }
    });

    btnAtualizar.addEventListener("click", carregarProdutos);

    // Carga inicial
    carregarProdutos();
});