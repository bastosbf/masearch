$.fn.isValid = function () {
  var value = $(this).val();
  return !isNaN(value) && value == parseInt(value);
};