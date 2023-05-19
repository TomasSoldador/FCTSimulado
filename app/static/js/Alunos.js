$(document).ready(function(){
   var selectedValue = $("#combobox").val();
   carregar_alunos(selectedValue);
})


$('#combobox').on('change', function () {
   var selectedValue = $(this).val();
   carregar_alunos(selectedValue)
});

function carregar_alunos(selectedValue) {
   $.ajax({
      url: "/get_alunos",
      type: "POST",
      data: JSON.stringify({
         "selected_value": selectedValue
      }),
      contentType: "application/json",
      success: function (response) {
         if (response.length == 0) {
            $('#tabela-alunos thead').hide();
            $('#tabela-alunos tbody').empty();
            $('.conteudo').hide();
            $('#frase').show();
         } else {
            $('.conteudo').show();
            $('#tabela-alunos thead').show();
            $('#tabela-alunos tbody').empty();
            $('#frase').hide();
            $.each(response, function (index, aluno) {
               var linha = $('<tr>');
               linha.append($('<td data-label="Nr">').text(aluno.nr));
               linha.append($('<td data-label="Nome">').text(aluno.nome));
               linha.append($('<td data-label="Nome abreviado">').text(aluno.nome_abreviado));
               linha.append($('<td data-label="Morada">').text(aluno.morada));
               linha.append($('<td data-label="Cód. postal">').text(aluno.cod_postal));
               linha.append($('<td data-label="Cartão cidadão">').text(aluno.cartao_cidadao));
               linha.append($('<td data-label="NIF">').text(aluno.nif));
               linha.append($('<td>').html(
                  '<a class="col-botoes" href="/Editar_Aluno/' + aluno.id + '"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"><path fill="white" fill-rule="evenodd" d="M15.586 3a2 2 0 0 1 2.828 0L21 5.586a2 2 0 0 1 0 2.828L19.414 10 14 4.586 15.586 3zm-3 3-9 9A2 2 0 0 0 3 16.414V19a2 2 0 0 0 2 2h2.586A2 2 0 0 0 9 20.414l9-9L12.586 6z" clip-rule="evenodd"/></svg></a>' +
                  '<a class="col-botoes" href="/EliminarAluno/' + aluno.id + '"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="white" class="bi bi-trash-fill" viewBox="0 0 16 16"><path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"/></svg></a>'));
               $('#tabela-alunos tbody').append(linha);
            });
         }
      },
      error: function (error) {
         console.error(error);
      }
   })
};
