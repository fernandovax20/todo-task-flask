function initializeSelect2(parent) {
    $('.select2_editable').each(function () {
        const selectElement = $(this);
        const selectId = selectElement.attr('id');
    
        selectElement.select2({
            placeholder: "Seleccione una opción",
            allowClear: true,
            dropdownParent: parent,
            tags: true,
            language: {
                noResults: function () {
                    return "Agregar: " + selectElement.data('select2').dropdown.$search.val();
                }
            },
            createTag: function (params) {
                var term = $.trim(params.term);
    
                if (term === '') {
                    return null;
                }
    
                var exists = false;
                selectElement.find('option').each(function () {
                    if ($.trim($(this).text()).toUpperCase() === term.toUpperCase()) {
                        exists = true;
                        return false;
                    }
                });
    
                if (!exists) {
                    return {
                        id: `new-${term}`, // Cambia el id temporalmente
                        text: "Agregar: " + term,
                        newTag: true,
                        selected: false
                    };
                }
    
                return null;
            },
            insertTag: function (data, tag) {
                data.push(tag);
            },
            templateSelection: formatStateSelected
        });
    
        function formatStateSelected(state) {
            if (!state.id) {
                return state.text;
            }
            
            if (state.id.startsWith('new-')) { 
                return state.text.replace('Agregar: ', ''); 
            }
            
            var $state = $(
                '<span>' + state.text + '</span>' +
                '<span class="icon-container">' +
                '<i class="fa-regular fa-circle-xmark clear-selection"></i>' +
                '<i class="fas fa-trash-alt remove-item"></i> ' +
                '</span>'
            );
    
            $state.find('.remove-item').on('mousedown', function (e) {
                e.preventDefault();
                e.stopPropagation();
    
                Swal.fire({
                    title: '¿Está seguro?',
                    text: '¿Desea eliminar esta opción?',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Sí, eliminar',
                    cancelButtonText: 'No, cancelar'
                }).then((result) => {
                    if (result.isConfirmed) {
                        const selectType = selectElement.data('select-type');
                        const optionId = state.id;
    
                        $.ajax({
                            url: `/delete_option`,
                            method: 'DELETE',
                            contentType: 'application/json',
                            data: JSON.stringify({
                                selectType: selectType,
                                optionId: optionId
                            }),
                            success: function (response) {
                                selectElement.find(`option[value="${optionId}"]`).remove();
                                selectElement.val(null).trigger('change');
                                selectElement.select2('close');
    
                                Swal.fire(
                                    'Eliminado!',
                                    'La opción ha sido eliminada.',
                                    'success'
                                );
                            },
                            error: function (xhr, status, error) {
                                console.error("Error al eliminar la opción:", status, error);
                            }
                        });
                    }
                });
            });
    
            $state.find('.clear-selection').on('mousedown', function (e) {
                e.preventDefault();
                e.stopPropagation();
                
                selectElement.val(null).trigger('change');  
                selectElement.select2('open');
            });
    
            return $state;
        }
    
        selectElement.on('select2:select', function (e) {
            const selectedOption = e.params.data;
            if (selectedOption.newTag) {
                const selectType = selectElement.data('select-type');
                const term = selectedOption.text.replace('Agregar: ', '');
                $.ajax({
                    url: `/add_option`,
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        selectType: selectType,
                        optionText: term
                    }),
                    success: function (response) {
                        const newOption = new Option(response.text, response.id, false, true);
                        selectElement.find(`option[value="new-${term}"]`).remove();  // Remover la opción temporal
                        selectElement.append(newOption).trigger('change');
                    },
                    error: function (xhr, status, error) {
                        console.error("Error al añadir la opción:", status, error);
                    }
                });
            }
        });
    });
    

    $('.select2_conFiltro').select2({
        placeholder: "Seleccione una opción",
        dropdownParent: parent,
        allowClear: true,
    });

    $('.select2_sinFiltro').select2({
        placeholder: "Seleccione una opción",
        allowClear: true,
        dropdownParent: parent,
        minimumResultsForSearch: Infinity,
    });
}
