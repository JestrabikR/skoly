var
  filters = {
    user: null,
    status: null,
    milestone: null,
    priority: null,
    tags: null
  };

function updateFilters() {
  $('.school-list-row').hide().filter(function() {
    var
      self = $(this),
      result = true;
    
    Object.keys(filters).forEach(function (filter) {
      if (filters[filter] && (filters[filter] != 'None') && (filters[filter] != 'Any')) {
        result = result && filters[filter] === self.data(filter);
      }
    });

    return result;
  }).show();
}

function changeFilter(filterName) {
  filters[filterName] = this.value;
  updateFilters();
}

$('#city').on('change', function() {
  changeFilter.call(this, 'user');
});

$('#school').on('change', function() {
  changeFilter.call(this, 'status');
});

$('#field').on('change', function() {
  changeFilter.call(this, 'milestone');
});

$('#tags-year').on('change', function() {
  changeFilter.call(this, 'tags');
});

/*
future use for a text input filter
$('#search').on('click', function() {
    $('.box').hide().filter(function() {
        return $(this).data('order-number') == $('#search-criteria').val().trim();
    }).show();
});*/