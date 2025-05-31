
let informazioni;
let contenuto = document.getElementById("contenuto");

let temiSaleArray = [];
let nomiSaleArray = [];

const params = new URLSearchParams(window.location.search);
const id_1 = params.get('id_1'); // Prende il valore di "id_1"
const id_2 = params.get('id_2'); // Prende il valore di "id_2"
if (id_1 == null && id_2 == null) {
   window.onload = function () {
      cerca(event);
   };
}




function cerca(event, id_1, id_2) {
    if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
   }
   window.history.replaceState({}, document.title, window.location.pathname);

   const form = document.querySelector("#form");
   const formData = new FormData(form);

   if (id_1 != null) {
      formData.append('Tema_Sala', `${id_1}`);
   } else if (id_2 != null) {
      formData.append('Codice', `${id_2}`);
   } 

   const obj = Object.fromEntries(formData)
   console.log(obj)
   console.log(formData)
   fetch('/museo/queries/select_sala/', {

      method: 'POST',
      header: {
         'Content-Type': 'application/json'
      },
      body:  JSON.stringify(obj)
   })

      .then(response => response.json())
      .then(data => {
         informazioni = data;
         console.log('dati ricevuti: ', data);
         let tabella = ` 
            <ul class="tabella">
               <nav class="fissa">
					   <li class="testata">
                     
						   
                     
						   <div class="col">Nome </div>
                     <div class="col">Superficie </div>
						   <div class="col">Tema Sala </div>
                     <div class="col">Numero di opere in sala </div>
					   </li>
               </nav>
                        ${generaRighe(data)}
                    </ul>
                    `;
         contenuto.innerHTML = tabella;
         // contenuto.insertAdjacentHTML('beforeend', tabella);
      })
      .catch((error) => {
         console.log('errore: ', error);
      });
}

function generaRighe(data) {
   let righe = '';
   let riga = '';
   let i = 0;
   generareTemisaleArray(event);
   generareNomiSaleArray(event);
   let classRiga = 'class="riga"';
   data.forEach(data => {
      if (i >= (pagina - 1) * 25 && i < pagina * 25) {
         riga = `
                <li ${classRiga}>
                     <div class="col"> ${data.nome} </div>
                     <div class="col"> ${data.superficie} </div>
                     <div class="col"><a href="/museo/tema?id_1=${data.temaSala}"> ${data.descrizione} </a></div>
                     <div class="col">  <a href="/museo/opera?id_2=${data.numero}">${data.Quadri_in_sala} </a></div>
                </tr>
                `;
      righe += riga;
      }
      i++;
   });
   numeroRighe = i;
   autocomplete(document.getElementById("n1"), nomiSaleArray);
   autocomplete(document.getElementById("t1"), temiSaleArray);
   return righe;

}

function canc(event) {
   document.getElementById('n1').value = "";
   document.getElementById('s1').value = "";
   document.getElementById('t1').value = "";
   cerca(event);
}

function generareTemisaleArray(event) {
   if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
   }
   window.history.replaceState({}, document.title, window.location.pathname);

   const form = document.querySelector("#form");
   const formData = new FormData(form);
   const obj = Object.fromEntries(formData)
   console.log(obj)
   console.log(formData)

   fetch('/museo/queries/select_sala/', {

      method: 'POST',
      header: {
         'Content-Type': 'application/json'
      },
      body: JSON.stringify(obj)
   })

      .then(response => response.json())
      .then(data => {
         informazioni = data;

         console.log('dati ricevuti: ', informazioni);

         let descrizione = [...new Set(informazioni.map(informazioni => informazioni.descrizione))];

         for (let i = 0; i < descrizione.length; i++) {
            temiSaleArray.push(`${descrizione[i]}`);
         }

      })
      .catch((error) => {
         console.log('errore: ', error);
      });
}

function generareNomiSaleArray(event) {
   if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
   }
   window.history.replaceState({}, document.title, window.location.pathname);

   const form = document.querySelector("#form");
   const formData = new FormData(form);
   const obj = Object.fromEntries(formData)
   console.log(obj)
   console.log(formData)

   fetch('/museo/queries/select_sala/', {

      method: 'POST',
      header: {
         'Content-Type': 'application/json'
      },
      body:  JSON.stringify(obj)
   })

      .then(response => response.json())
      .then(data => {
         informazioni = data;

         console.log('dati ricevuti: ', informazioni);

         let nome = [...new Set(informazioni.map(informazioni => informazioni.nome))];

         for (let i = 0; i < nome.length; i++) {
            nomiSaleArray.push(`${nome[i]}`);
         }

      })
      .catch((error) => {
         console.log('errore: ', error);
      });
}