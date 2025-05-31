
let informazioni;
let contenuto = document.getElementById("contenuto");

let descrizioneArray = [];

const params = new URLSearchParams(window.location.search);
const id_1 = params.get('id_1'); // Prende il valore di "id_1"
if (id_1 == null ) {
   window.onload = function () {
      cerca(event);
   };
}


function cerca(event, id) {
    if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
   }
   window.history.replaceState({}, document.title, window.location.pathname);
   console.log(id)
   const form = document.querySelector("#form");
   const formData = new FormData(form);

   if (id != null) {
      formData.append('Codice', `${id}`);
   } 

   const obj = Object.fromEntries(formData)
   console.log(obj)
   console.log(formData)
  fetch('/museo/queries/select_tema/', {
   method: 'POST',
   headers: {
      'Content-Type': 'application/json'
      
   },
   body: JSON.stringify(obj)
})
.then(response => response.json())
.then(data => {
   informazioni = data;
   console.log('dati ricevuti: ', data);
   let tabella = ` 
      <ul class="tabella">
         <nav class="fissa">
            <li class="testata">
               <div class="col">Descrizione </div>
               <div class="col">Numero di sale con questo tema </div>
            </li>
         </nav>
         ${generaRighe(data)}
      </ul>
   `;
   contenuto.innerHTML = tabella;
})
.catch((error) => {
   console.log('errore: ', error);
});
}

function generaRighe(data) {
   let righe = '';
   let riga = '';
   let i = 0;
   generareDescrizioneArray(event);
   let classRiga = 'class="riga"';
   data.forEach(data => {
      if (i >= (pagina - 1) * 25 && i < pagina * 25) {
         riga = `
                <li ${classRiga}>
                     
                    
                     <div class="col"> ${data.descrizione} </div>
                      <div class="col"><a href="/museo/sala?id_1=${data.descrizione}"> ${data.conteggio} </a></div>
                     
                </li>
                `;
      righe += riga;
      }
   i++;
   });
   numeroRighe = i;
   autocomplete(document.getElementById("n1"), descrizioneArray);
   return righe;

}

function canc(event) {
   event.preventDefault();
   document.getElementById('n1').value = "";
   cerca(event);
}

function generareDescrizioneArray(event) {
   if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
   }
   window.history.replaceState({}, document.title, window.location.pathname);

   const form = document.querySelector("#form");
   const formData = new FormData(form);
   const obj = Object.fromEntries(formData)
   console.log(obj)
   console.log(formData)

   fetch('/museo/queries/select_tema/', {

      method: 'POST',
      headers: {
         'Content-Type': 'application/json'
      },
      body:  JSON.stringify(obj)
   })

      .then(response => response.json())
      .then(data => {
         informazioni = data;

         console.log('dati ricevuti: ', informazioni);

         let descrizione = [...new Set(informazioni.map(informazioni => informazioni.descrizione))];

         for (let i = 0; i < descrizione.length; i++) {
            descrizioneArray.push(`${descrizione[i]}`);
         }

      })
      .catch((error) => {
         console.log('errore: ', error);
      });
}






