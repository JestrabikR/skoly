var
  filters = {
    city: null,
    school: null,
    field: null,
    year: null,
  };

function updateFilters() {
  $('.school-list-row').hide().filter(function() {
    var
      self = $(this),
      result = true;
    
    Object.keys(filters).forEach(function (filter) {
      console.log(filters[filter] === self.data(filter))
      if (filters[filter] && (filters[filter] != 'Všechny')) {
        result = result && filters[filter] === self.data(filter);
      }
    });
    console.log(result)
    return result;
  }).show();
}

function changeFilter(filterName) {
  filters[filterName] = this.value;
  updateFilters();
}

$('#city').on('change', function() {
  changeFilter.call(this, 'city');
});

$('#school').on('change', function() {
  changeFilter.call(this, 'school');
});

$('#field').on('change', function() {
  changeFilter.call(this, 'field');
});

$('#year').on('change', function() {
  changeFilter.call(this, 'year');
});