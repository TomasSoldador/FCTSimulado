function limitarInput(input) {
   if (input.value.length > 8) {
      input.value = input.value.slice(0, 8);
   }
}

function limitarInput2(input) {
   if (input.value.length > 9) {
      input.value = input.value.slice(0, 9);
   }
}

function limitarInput3(input) {
   if (input.value.length > 6) {
      input.value = input.value.slice(0, 6);
   }
}