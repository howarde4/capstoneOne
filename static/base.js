const BASE_URL = "http://www.nokeynoshade.party/api/queens?name=";

async function processForm(evt) {
    evt.preventDefault();

    let name = $("#name").val();
    const queenRes = await axios.get(`${BASE_URL}${name}`);
    if (queenRes.data[0] === undefined) {
        const $error = $('#error')
        $error.html("Sorry, no shade but cannot find that queen! Try a different name.");
        setTimeout(function() {
            $error.fadeOut().empty().fadeIn();
        }, 3000);
    } else {
        let dragQueen = $(handleResponse(queenRes.data[0]));
        $("#queenDiv").append(dragQueen)
        $("#queenForm").trigger("reset");
    }
}

function handleResponse(resp) {
    let name = resp.name
    let image = resp.image_url
    let quote = resp.quote
    return `
    <div class="card-deck" style="width: 25%;">
        <div class="card mb-3" style="max-width: 18rem;border: 5px solid rgb(75, 3, 241);">
            <div class="card-body d-flex flex-column justify-content-between">
                <h3 class="card-title" id="dragName">
                    ${name}
                </h3>
                <img src=${image} id="dragImage" class="card-img-top">
            </div>
            <div id="quote" class="card-footer bg-transparent border-info">
                "${quote}"
            </div>
            <button type="button" id="queenBtn" class="btn btn-primary btn-lg btn-block">
                Add Queen!
            </button>
        </div>
    </div>`;
}

$("#queenForm").on("submit", processForm);


$("#queenDiv").on("click", "#queenBtn", async function(evt){
    let $card = $(evt.target).closest(".card");
    let $name = $card.find('#dragName').text();
    let name = $.trim($name)
    let image = $card.find('img').attr('src');
    let $quote = $card.find('#quote').text();
    let quote = $.trim($quote)
    let $username = $(evt.target).closest("#queenDiv");
    let username = $username.attr("data-user-name");

    const newAllstarRes = await axios.post(`http://127.0.0.1:5000/users/${username}/allstars`, {
                name,
                image,
                quote,
                username
            });
            
    window.location.href = `http://127.0.0.1:5000/users/${username}/allstars`;
});