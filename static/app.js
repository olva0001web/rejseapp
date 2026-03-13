document.addEventListener("DOMContentLoaded", () => {

    const toggleBtn = document.getElementById("toggle-travel-form")
    const panel = document.getElementById("travel-form-container")

    // OPEN CREATE FORM
    toggleBtn.addEventListener("click", async () => {

        const res = await fetch("/travel/create/panel")
        const html = await res.text()

        panel.innerHTML = html
        panel.style.display = "block"

        //remove active on previously clicked card
        document.querySelectorAll(".travel-card").forEach(c => c.classList.remove("active"))

        loadCountries()
        attachCreateTravelHandler()

    })


    // OPEN TRAVEL DETAILS
    document.querySelector(".travel-card-container").addEventListener("click", async (e) => {

        const card = e.target.closest(".travel-card")

        if(!card) return
        
        //remove active on previously clicked card
        document.querySelectorAll(".travel-card").forEach(c => c.classList.remove("active"))

        // activate the clicked card
        card.classList.add("active")

        const id = card.dataset.id

            const res = await fetch(`/travel/${id}/panel`)
            const html = await res.text()

            panel.innerHTML = html
            panel.style.display = "block"

    })

})




function attachCreateTravelHandler(){

    const form = document.querySelector("#travel-form-container form")
    if(!form) return

    form.addEventListener("submit", async (e) => {

        e.preventDefault()

        const data = new FormData(form)
        const travel_pk = data.get("travel_pk")

        let url = "/api-create-travel"
        let method = "POST"

        if(travel_pk){
            url = `/travel/${travel_pk}`
            method = "PATCH"
        }

        const res = await fetch(url,{
            method: method,
            body: data
        })

        if(!res.ok){
            alert("Failed to save travel")
            return
        }

        const html = await res.text()

        if(method === "POST"){

            const container = document.querySelector(".travel-card-container")
            container.insertAdjacentHTML("afterbegin", html)

        } else {

            const card = document.querySelector(`[data-id="${travel_pk}"]`)
            if(card) card.outerHTML = html

        }

        const panel = document.getElementById("travel-form-container")
        panel.innerHTML = ""
        panel.style.display = "none"

    })
}



function openDeleteModal(id){
    const modal = document.getElementById(`delete-modal-${id}`)
    if(modal){
        modal.style.display = "flex"
    }
}


function closeDeleteModal(id){
    const modal = document.getElementById(`delete-modal-${id}`)
    if(modal){
        modal.style.display = "none"
    }
}



async function deleteTravel(id){

    const res = await fetch(`/travel/${id}`, {
        method: "DELETE"
    })

    if(!res.ok){
        alert("Failed to delete travel")
        return
    }

    const card = document.querySelector(`[data-id="${id}"]`)
    if(card){
        card.remove()
    }

    const panel = document.getElementById("travel-form-container")
    if(panel){
        panel.innerHTML = ""
        panel.style.display = "none"
    }

}



async function loadCountries(){

    const select = document.getElementById("country-select")
    if(!select) return

    const res = await fetch("https://restcountries.com/v3.1/all?fields=name,cca2")
    const countries = await res.json()

    countries.sort((a,b)=>a.name.common.localeCompare(b.name.common))

    countries.forEach(country => {

        const option = document.createElement("option")

        option.value = country.name.common
        option.textContent = country.name.common
        option.dataset.code = country.cca2.toLowerCase()

        select.appendChild(option)

    })

    // apply selected country when editing
    const selected = select.dataset.selected

    if(selected){
        select.value = selected

        const option = select.querySelector(`option[value="${selected}"]`)
        if(option){
            document.getElementById("country-code").value = option.dataset.code
        }
    }

    new TomSelect("#country-select",{

        render:{

            option:function(data,escape){

                const option = select.querySelector(`option[value="${data.value}"]`)
                const code = option.dataset.code

                return `
                <div>
                    <img src="https://flagcdn.com/24x18/${code}.png" style="margin-right:8px;">
                    ${escape(data.text)}
                </div>
                `
            },

            item:function(data,escape){

                const option = select.querySelector(`option[value="${data.value}"]`)
                const code = option.dataset.code

                return `
                <div>
                    <img src="https://flagcdn.com/24x18/${code}.png" style="margin-right:8px;">
                    ${escape(data.text)}
                </div>
                `
            }

        },

        onChange:function(value){

            const option = select.querySelector(`option[value="${value}"]`)
            document.getElementById("country-code").value = option.dataset.code

        }

    })

}


async function openUpdateTravel(id){

    const panel = document.getElementById("travel-form-container")

    const res = await fetch(`/travel/${id}/edit/panel`)
    const html = await res.text()

    panel.innerHTML = html
    panel.style.display = "block"

    loadCountries()
    attachCreateTravelHandler()

}