$(document).ready(function () {
   var nome_entidade = $("#combo_box_entidade").val();
   carregar_dados(nome_entidade);

   var selectedValue = $("#combo_box_turma").val();
   carregar_alunos(selectedValue);

   $("#combo_box_entidade").on('change', function () {
      var nome_entidade = $(this).val();
      carregar_dados(nome_entidade);
   });

   $('#combo_box_turma').on('change', function () {
      var selectedValue = $(this).val();
      carregar_alunos(selectedValue);
   });

   function carregar_dados(nome_entidade) {
      $.ajax({
         url: "/get_info_entidade",
         type: "POST",
         data: JSON.stringify({
            "nome_entidade": nome_entidade
         }),
         contentType: "application/json",
         success: function (response) {
            $('#morada').val(response.morada);
            $('#cod_postal').val(response.cod_postal);
            $('#localidade').val(response.localidade);
         },
         error: function (xhr, status, error) {
            console.error(error);
         }
      });
   }

   function carregar_alunos(selectedValue) {
      $.ajax({
         url: "/get_options",
         type: "POST",
         dataType: "json",
         data: JSON.stringify({
            "selected_value": selectedValue
         }),
         contentType: "application/json",
         success: function (response) {
            $('#combo_box_alunos').empty();
            if (response.length == 0) {
               $('#combo_box_alunos').append('<option value="nenhum">Não há alunos</option>');
            } else {
               $('#combo_box_alunos').append('<option value="" disabled>Alunos</option>');
               for (var i = 0; i < response.length; i++) {
                  var aluno = response[i];
                  $('#combo_box_alunos').append('<option value="' + aluno.id + '">' + aluno.nome + '</option>');
               }
            }
         },
         error: function (xhr, status, error) {
            console.error(error);
         }
      });
   }

   $("#data_inicio").change(function () {
      var data_inicio = new Date($(this).val());
      var dias_uteis = 0;
      while (dias_uteis < 64) {
         data_inicio.setDate(data_inicio.getDate() + 1);
         if (data_inicio.getDay() !== 0 && data_inicio.getDay() !== 6) {
            dias_uteis++;
         }
      }
      var data_fim_str = data_inicio.toISOString().substring(0, 10);
      $("#data_fim").val(data_fim_str);
   });

   $("#cod_postal").on('input', function(){
      let cp = $(this).val();
      cp = cp.replace(/\D/g, '');
      cp = cp.substring(0, 4) + (cp.length > 4 ? '-' + cp.substring(4) : '');
      $(this).val(cp);
   })

   
});

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
      url: '/Editar_Estagio/' + $(this).attr('estagio_id'),
      method: 'POST',
      data: DataForms,
      success: function(response) {
         if(response[0] === "0"){
            window.location.href = "/Estagios";
         }else{
            showCustomToast(response[0]);
         }
      },
      error: function(xhr, status, error) {
         console.error(error);
      }
   });
});

