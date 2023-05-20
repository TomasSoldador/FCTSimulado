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

$('#forms').submit(function(event) {
   event.preventDefault();
   var DataForms = $(this).serialize();
   $.ajax({
      url: '/Novo_Estagio',
      method: 'POST',
      data: DataForms,
      success: function(response) {
         if(response[0] === "0"){
            window.location.href = "/Estagios";
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

