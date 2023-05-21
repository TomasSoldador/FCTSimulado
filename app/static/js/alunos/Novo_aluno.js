let isToastVisible = false;

function showCustomToast(mensagem) {
   if (!isToastVisible) {
      Toastify({
         text: mensagem,
         className: "custom-toastify",
      }).showToast();

      isToastVisible = true;

      setTimeout(function() {
         isToastVisible = false;
      }, 3000);
   }
}

$('#forms').submit(function(event) {
   event.preventDefault();
   var DataForms = $(this).serialize();
   $.ajax({
      url: '/Novo_Aluno',
      method: 'POST',
      data: DataForms,
      success: function(response) {
         if(response[0] === "0"){
            window.location.href = "/Alunos";
         }else{
            showCustomToast(response[0]);
         }
      },
      error: function(xhr, status, error) {
         console.error(error);
      }
   });
});
