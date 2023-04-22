const mensagem = document.getElementById("mensagem");
setTimeout(() => {
   mensagem.classList.add("visivel");
}, 500);
setTimeout(() => {
   mensagem.classList.remove("visivel");
   mensagem.classList.add("escondido");
}, 4000);
