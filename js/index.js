/**
 * Updates the amendments table with the provided data.
 *
 * @param {Object} data - The data containing amendments information.
 * @param {Array} data.amendments - An array of amendment objects.
 * @param {string} data.amendments[].author - The author of the amendment.
 * @param {string} data.amendments[].local - The local associated with the amendment.
 * @param {string} data.amendments[].function - The function or purpose of the amendment.
 * @param {number} data.amendments[].value - The monetary value of the amendment.
 * @param {number} data.amendments[].year - The year the amendment was made.
 */
function displayAmendments(data) {
    const tableElement = document.getElementById('amendments-table');
    let rows = '';

    if(data == null || data.amendments == undefined){
        tableElement.innerHTML = rows;
        return;
    };

    data.amendments.forEach((amendment) => {
        rows += `<tr>
                <td>${amendment.author}</td>
                <td>${amendment.local}</td>
                <td>${amendment.function}</td>
                <td><b>R$ </b>${amendment.value.toLocaleString('pt-BR')}</td>
                <td>${amendment.year}</td>
                </tr>`;
    });
    tableElement.innerHTML = rows;
};

/**
 * Fetches amendments based on the specified search type and parameter.
 *
 * @param {string} searchType - The type of search to perform ('local', 'author-name' or 'function').
 * @param {string} searchParam - The parameter to search for.
 * @param {number} [page=0] - The page number to fetch (default is 0).
 * @param {number} [pageSize=100] - The number of items per page (default is 100).
 * @returns {Promise<void>} - A promise that resolves when the fetch operation is complete.
 */
async function fetchAmendments(searchType, searchParam, page=0, pageSize=100, sortOrdering='true', sortKey='value') {
    let url = `https://pesquisador-de-emendas.onrender.com/${searchType}/${searchParam}/?page=${page}&page_size=${pageSize}&ascending=${sortOrdering}&sort_key=${sortKey}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        displayAmendments(data);
    } catch (error) {
        console.error("Erro ao realizar a busca:", error);
        displayAmendments(null);
    }
};

/**
 * Asynchronously retrieves the page parameters from the DOM.
 *
 * This function fetches the values of the elements with IDs 'page' and 'page-size'
 * and returns them as an object containing `page` and `pageSize` properties.
 *
 * @returns {Promise<{page: string, pageSize: string}>} A promise that resolves to an object containing the page parameters.
 */
async function getPageParameters(){
    const page = document.getElementById('page').value;
    const pageSize = document.getElementById('page-size').value;
    const sortOrdering = document.querySelector('input[name="sort-ordering"]:checked').value;
    const sortKey = document.querySelector('input[name="sort-key"]:checked').value;
    return {page, pageSize, sortOrdering, sortKey};
};


/**
 * Submits a search request based on the selected search type and parameters.
 * 
 * This function retrieves the selected search type from radio buttons, the search parameter from an input field,
 * and additional parameters from the `getPageParameters` function. It then logs these values and calls the 
 * `fetchAmendments` function with appropriate arguments based on the search type.
 * 
 * @async
 * @function sumbitSearch
 * @returns {Promise<void>} - A promise that resolves when the search request is completed.
 */
async function sumbitSearch(){
    const searchType = document.querySelector('input[name="search-type"]:checked').value;
    const searchParam = document.getElementById('param').value;
    const additionalParams = await getPageParameters();
    
    if(searchType == 'local'){ 
        fetchAmendments('search-by-local', searchParam, 
            additionalParams.page, additionalParams.pageSize, additionalParams.sortOrdering, additionalParams.sortKey);
    }
    else if(searchType == 'author-name'){
        fetchAmendments('search-by-author', searchParam, 
            additionalParams.page, additionalParams.pageSize, additionalParams.sortOrdering, additionalParams.sortKey);
    }
    else if(searchType == 'function'){
        fetchAmendments('search-by-function', searchParam,
            additionalParams.page, additionalParams.pageSize, additionalParams.sortOrdering, additionalParams.sortKey);
    };
};

/*--------------------------------------------
                EVENT LISTENERS
--------------------------------------------*/

const increasePageButton = document.getElementById('increase-page');    
const decreasePageButton = document.getElementById('decrease-page');
const submitButton = document.getElementById('submit-button');

increasePageButton.addEventListener('click', () => {
    const pageElement = document.getElementById('page');
    pageElement.value = parseInt(pageElement.value) + 1;
    sumbitSearch();
});

decreasePageButton.addEventListener('click', () => {
    const pageElement = document.getElementById('page');
    let newVal = parseInt(pageElement.value) - 1;
    if(newVal >= 0){
        pageElement.value = newVal;
    }
    sumbitSearch();
});

submitButton.addEventListener('click', sumbitSearch);


