const LOCAL_FORM = `
    <form id='searchForm' onSubmit="return false;">
        <label>Local:</label>
        <select id="param">
            <option value="AC">Acre (AC)</option>
            <option value="AL">Alagoas (AL)</option>
            <option value="AP">Amapá (AP)</option>
            <option value="AM">Amazonas (AM)</option>
            <option value="BA">Bahia (BA)</option>
            <option value="CE">Ceará (CE)</option>
            <option value="DF">Distrito Federal (DF)</option>
            <option value="ES">Espírito Santo (ES)</option>
            <option value="GO">Goiás (GO)</option>
            <option value="MA">Maranhão (MA)</option>
            <option value="MT">Mato Grosso (MT)</option>
            <option value="MS">Mato Grosso do Sul (MS)</option>
            <option value="MG">Minas Gerais (MG)</option>
            <option value="PA">Pará (PA)</option>
            <option value="PB">Paraíba (PB)</option>
            <option value="PR">Paraná (PR)</option>
            <option value="PE">Pernambuco (PE)</option>
            <option value="PI">Piauí (PI)</option>
            <option value="RJ">Rio de Janeiro (RJ)</option>
            <option value="RN">Rio Grande do Norte (RN)</option>
            <option value="RS">Rio Grande do Sul (RS)</option>
            <option value="RO">Rondônia (RO)</option>
            <option value="RR">Roraima (RR)</option>
            <option value="SC">Santa Catarina (SC)</option>
            <option value="SP">São Paulo (SP)</option>
            <option value="SE">Sergipe (SE)</option>
            <option value="TO">Tocantins (TO)</option>
        </select>
    </form>
`
const AUTHOR_FORM = `
        <form id="searchForm" onSubmit="return false;">
            <label>Nome do autor:</label>
            <input type="text" id="param">
        </form>
`
const FUNCTION_FORM = `
    <form id="searchForm" onSubmit="return false;">
        <label>Nome da função:</label>
        <select id="param">
            <option value="Saúde">Saúde</option>
            <option value="Educação">Educação</option>
            <option value="Urbanismo">Urbanismo</option>
            <option value="Agricultura">Agricultura</option>
            <option value="Assistência social">Assistência Social</option>
            <option value="Outros">Outros</option>
        </select>
    </form>
`

function getSearchType(){
    return document.querySelector('input[name="search-type"]:checked').value;
}

function showCorrespondentForm(searchType){
    const formDiv = document.getElementById('search-form');

    if(searchType == 'local'){
        formDiv.innerHTML = LOCAL_FORM;}
    else if(searchType == 'author-name'){
        formDiv.innerHTML = AUTHOR_FORM;}
    else if(searchType == 'function'){
        formDiv.innerHTML = FUNCTION_FORM;}
};

function updateSearchForm(){
    let searchType = getSearchType();
    showCorrespondentForm(searchType);
};

const search_by_author_form_button = document.getElementById('author-search-button');
const search_by_function_form_button = document.getElementById('function-search-button');
const search_by_local_form_button = document.getElementById('local-search-button');

search_by_author_form_button.addEventListener('click', updateSearchForm);
search_by_function_form_button.addEventListener('click', updateSearchForm);
search_by_local_form_button.addEventListener('click', updateSearchForm);

updateSearchForm();




