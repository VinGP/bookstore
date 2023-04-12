const loadAutocomplete = (q) => {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/autocomplete/' + q, false,);

    xhr.send();
    let response = JSON.parse(xhr.responseText);
    return response.data


}

function debounce(callee, timeoutMs) {

    return function perform(...args) {
        console.log("get")

        let previousCall = this.lastCall

        this.lastCall = Date.now()

        if (previousCall && this.lastCall - previousCall <= timeoutMs) {
            clearTimeout(this.lastCallTimer)
        }

        this.lastCallTimer = setTimeout(() => callee(...args), timeoutMs)

    }
}


db_load = debounce(loadAutocomplete, 250)
function autocomplete() {

    let currentFocus;

    let inp = document.getElementById("searchInput")

    inp.addEventListener("input", debounce(function (e) {
        console.log("input")
        inp = document.getElementById("searchInput")
        let a, b, i, val = inp.value;

        closeAllLists();
        if (!val) {
            return false;
        }

        $.ajax({
            type: 'get',
            url: "/autocomplete/" + val,
            context: document.body,
            contentType: 'application/json',
            success: function (data) {
                let arr = data.data
                currentFocus = -1;
                a = document.createElement("DIV");
                a.setAttribute("id", inp.id + "autocomplete-list");
                a.setAttribute("class", "autocomplete-items");
                inp.parentNode.appendChild(a);
                console.log(arr)
                for (i = 0; i < arr.length; i++) {
                    b = document.createElement("DIV");
                    b.innerHTML = arr[i]
                    b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                    b.addEventListener("click", function (e) {
                        inp = document.getElementById("searchInput")
                        inp.value = this.getElementsByTagName("input")[0].value;
                        document.getElementById("searchBtn").click();
                        closeAllLists();
                    });
                    a.appendChild(b);

                }
            }
        });

    }, 400));
    inp.addEventListener("keydown", function (e) {
        var x = document.getElementById(inp.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode === 40) {

            currentFocus++;
            addActive(x);

            inp.value = x[currentFocus].getElementsByTagName("input")[0].value.replaceAll('<strong>', '').replaceAll('</strong>', '').replaceAll('|', '')
        } else if (e.keyCode === 38) {
            currentFocus--;
            addActive(x);

            console.log(x)
            console.log(x[currentFocus])
            inp.value = x[currentFocus].getElementsByTagName("input")[0].value.replaceAll('<strong>', '').replaceAll('</strong>', '').replaceAll('| ', '')
        } else if (x && e.keyCode === 13) {
            e.preventDefault()

            if (currentFocus > -1) {
                document.getElementById("searchBtn").click();
            }
            else {
                document.getElementById("searchBtn").click();
            }

        }
    });

    function addActive(x) {

        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        let x = document.getElementsByClassName("autocomplete-items");
        for (let i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}




autocomplete();

// https://doka.guide/js/debounce/
// https://chrisboakes.com/how-a-ja vascript-debounce-function-works/
// https://stackoverflow.com/questions/53603611/submitting-query-from-the-autocomplete-list-without-having-to-hit-the-submit-but