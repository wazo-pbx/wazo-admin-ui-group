$(document).ready(function () {
  $('.group-context').on("change", function (e) {
    add_available_extensions();
  });
  add_available_extensions();
});

function add_available_extensions() {
  let extension_select = $(".group-exten")
  let context_select = $(".group-context")
  let ajax_url = $(extension_select).attr('data-available_extension_href')
  if (!ajax_url) {
    return;
  }

  extension_select.select2('data', null);
  if (!extension_select.val()) {
    extension_select.append("<option></option>")
  }

  extension_select.select2({
    allowClear: true,
    theme: 'bootstrap',
    placeholder: 'Select...',
    ajax: {
      url: ajax_url,
      data: function (params) {
        return {
          term: params.term,
          context: context_select.val()
        }
      },
    },
    processResults: function (data, page) {
      return {
        results: data
      };
    }
  });
}