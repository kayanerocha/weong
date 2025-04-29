function setValueInput(idInput, value) {
    const inputElement = document.getElementById(idInput);
    inputElement.value = value;
}

function pesquisarCep() {
    const cep = document.getElementById('cep').value;
    const apiUrl = `https://brasilapi.com.br/api/cep/v2/${cep}`;
    fetch(apiUrl).then(response => {
        if (!response.ok) {
            throw new Error('Erro ao consultar o CNPJ.')
        }
        return response.json();
    }).then(data => {
        setValueInput('logradouro', data.street);
        setValueInput('bairro', data.neighborhood);
        setValueInput('cidade', data.city);
        setValueInput('estado', data.state);
        setValueInput('cep', data.cep);
    }).catch(error => {
        console.error('Error: ', error);
    });
}

function setValueInput(idInput, value) {
    const inputElement = document.getElementById(idInput);
    inputElement.value = value;
}

function pesquisarCnpj() {
    const cep = document.getElementById('cnpj').value;
    const apiUrl = `https://brasilapi.com.br/api/cnpj/v1/${cep}`;
    fetch(apiUrl).then(response => {
        if (!response.ok) {
            throw new Error('Erro ao consultar o CNPJ.')
        }
        return response.json();
    }).then(data => {
        setValueInput('nome_fantasia', data.nome_fantasia);
        setValueInput('razao_social', data.razao_social);
        setValueInput('logradouro', `${data.descricao_tipo_de_logradouro} ${data.logradouro}`);
        setValueInput('numero', data.numero);
        setValueInput('complemento', data.complemento);
        setValueInput('bairro', data.bairro);
        setValueInput('cidade', data.municipio);
        setValueInput('estado', data.uf);
        setValueInput('cep', data.cep);
    }).catch(error => {
        console.error('Error: ', error);
    });
}