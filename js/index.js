function displayAmendments(data) {
    const tableElement = document.getElementById('amendments-table');
    let rows = '';

    if(data == null){
        tableElement.innerHTML = rows;
        return;
    };

    data.amendments.forEach((amendment) => {
        rows += `<tr>
                <td>${amendment[4]}</td>
                <td>${amendment[2]}</td>
                <td>${amendment[3]}</td>
                <td>${amendment[1].toFixed(2)}</td>
                <td>${amendment[5]}</td>
                </tr>`;
    });
    tableElement.innerHTML = rows;
};

async function searchAmendments(searchType, searchParam) {
    try {
        const response = await fetch(`http://localhost:8000/${searchType}/${searchParam}`);
        const data = await response.json();
        displayAmendments(data);
    } catch (error) {
        console.error("Erro ao realizar a busca:", error);
        displayAmendments(null);
    }
}

const submitButton = document.getElementById('submit-button');

async function sumbitSearch(){
    const searchType = document.querySelector('input[name="search-type"]:checked').value;
    const searchParam = document.getElementById('param');

    if(searchType === 'local'){ 
        searchAmendments('search-by-local', searchParam.value);
    }
    else if(searchType === 'author-name'){
        searchAmendments('search-by-author', searchParam.value);
    }
    else if(searchType === 'function'){
        searchAmendments('search-by-function', searchParam.value);
    }
}

submitButton.addEventListener('click', sumbitSearch);