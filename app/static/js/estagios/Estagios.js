$(document).ready(function(){
   var selectedValue = $("#combobox").val();
   carregar_alunos(selectedValue);
});


$('#combobox').on('change', function () {
   var selectedValue = $(this).val();
   carregar_alunos(selectedValue);
});

function carregar_alunos(selectedValue) {
   $.ajax({
      url: "/get_estagios",
      type: "POST",
      data: JSON.stringify({
         "selected_value": selectedValue
      }),
      contentType: "application/json",
      success: function (response) {
         if (response.length == 0) {
            $('#tabela-estagios thead').hide();
            $('#tabela-estagios tbody').empty();
            $('.conteudo').hide();
            $('#frase').show();
         } else {
            $('#tabela-estagios thead').show();
            $('#tabela-estagios tbody').empty();
            $('.conteudo').show();
            $('#frase').hide();
            $.each(response, function (index, estagio) {
               var linha = $('<tr>');
               linha.append($('<td data-label="Aluno">').text(estagio.nome_abreviado));
               linha.append($('<td data-label="Entidade">').text(estagio.entidade));
               linha.append($('<td data-label="Data inicio">').text(estagio.data_inicio));
               linha.append($('<td data-label="Data fim">').text(estagio.data_fim));
               linha.append($('<td>').html(
                  '<a class="col-botoes" href="Home"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white" class="bi bi-eye-fill" viewBox="0 0 16 16"><path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z" /><path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z" /></svg></a>' +
                  '<a class="col-botoes" href="/Editar_Estagio/' + estagio.id + '"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M15.586 3a2 2 0 0 1 2.828 0L21 5.586a2 2 0 0 1 0 2.828L19.414 10 14 4.586 15.586 3zm-3 3-9 9A2 2 0 0 0 3 16.414V19a2 2 0 0 0 2 2h2.586A2 2 0 0 0 9 20.414l9-9L12.586 6z" clip-rule="evenodd"/></svg></a>' +
                  '<a class="col-botoes" href="/Eliminar_Estagio/' + estagio.id + '"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white" class="bi bi-trash-fill" viewBox="0 0 16 16"><path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/></svg></a>' +
                  '<a class="col-botoes" href="#" onclick="executarFuncao(' + estagio.id + ')" ><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white" class="bi bi-download" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z" /><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z" /></svg></a>'));
               $('#tabela-estagios tbody').append(linha);
            });
         }
      },
      error: function (xhr, status, error) {
         console.error(error);
      }
   })};

   function executarFuncao(id) {
      window.location.href = '/Baixar/' + id;
   }

