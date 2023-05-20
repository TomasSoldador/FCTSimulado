$('#forms').submit(function(event) {
   event.preventDefault();
   var DataForms = $(this).serialize();
   $.ajax({
      url: '/Nova_Entidade',
      method: 'POST',
      data: DataForms,
      success: function(response) {
         if(response[0] === "0"){
            window.location.href = "/Entidades";
         }else{
            mensagem = response[0]
            //TODO:mudar para uma cor de aviso
            Toastify({
               text: mensagem,
               duration : 3000,
               position: "bottom-right",
               stopOnFocus: true,
               style: {
                  background: "linear-gradient(to right, #00b09b, #96c93d)",
               }
            }).showToast();
         }
      },
      error: function(xhr, status, error) {
         console.error(error);
      }
   });
});