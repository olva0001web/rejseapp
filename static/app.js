document.getElementById("toggle-travel-form").addEventListener("click", function(){
    const form = document.getElementById("travel-form-container")

    if(form.style.display === "none"){
        form.style.display = "block"
    } else {
        form.style.display = "none"
    }
})


async function loadCountries(){

const res = await fetch("https://restcountries.com/v3.1/all?fields=name,cca2")
const countries = await res.json()

countries.sort((a,b)=>a.name.common.localeCompare(b.name.common))

const select = document.getElementById("country-select")

countries.forEach(country=>{

const option = document.createElement("option")
option.value = country.cca2
option.textContent = country.name.common

select.appendChild(option)

})

new TomSelect("#country-select",{

render:{

option:function(data,escape){

const code = data.value.toLowerCase()

return `
<div>
<img src="https://flagcdn.com/24x18/${code}.png" style="margin-right:8px;">
${escape(data.text)}
</div>
`
},

item:function(data,escape){

const code = data.value.toLowerCase()

return `
<div>
<img src="https://flagcdn.com/24x18/${code}.png" style="margin-right:8px;">
${escape(data.text)}
</div>
`
}

}

})

}

loadCountries()