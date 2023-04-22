function formatar(cpInput) {
   let cp = cpInput.value;
   cp = cp.replace(/\D/g, '');
   cp = cp.substring(0, 4) + (cp.length > 4 ? '-' + cp.substring(4) : '');
   cpInput.value = cp;
}