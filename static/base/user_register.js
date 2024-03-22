$(".default-select2").select2({
  width: "100%",
  allowClear: true,
  placeholder: "Seleccione una opción",
  minimumResultsForSearch: -1,
});

$(".multiple-select2").select2({
  width: "100%",
  allowClear: true,
  placeholder: "Seleccione sus opciones",
  multiple: true,
  minimumResultsForSearch: -1,
});

const carrersQuery = `
  query select2Queries {
    select2 {
      carreers {
        id
        text
        __typename
      }
    }
  }
`;

const specializationsQuery = `query select2Queries {
    select2 {
      specializations {
        id
        text
        __typename
      }
    }
  }`;

const languageQuery = `query select2LanguagesQueries {
    select2 {
      languages {
        id
        text
        __typename
      }
    }
  }`;

const citiesQuery = `query select2Queries {
  select2 {
    cities {
      id
      text
      __typename
    }
  }
}`;

const newUserMutation = `
mutation newProfessionalMutations($input: MutationUserInput!) {
  psychology {
    newProfessional(input: $input) {
      __typename
      ... on ProfessionalType {
        __typename
        originalId
        firstName
        lastName
        email
        avatar {
          originalId
          url
          __typename
        }
        genderEnum
        facebookProfile
        instagramProfile
        linkedinProfile
        userCarreerSet {
          originalId
          name
          description
          serviceMethodEnum
          serviceModalityEnum
          truncateExperienceSummary
          __typename
        }
        userSpecializationSet {
          originalId
          name
          description
          __typename
        }
        languagesSet {
          name
          slug
          __typename
        }
        userOfficeSet {
          name
          city {
            name
            __typename
          }
          __typename
        }
        attachmentSet {
          originalId
          url
          description
        }
        isVerifiedProfile
        profileUrl
        __typename
      }
      ... on ResponseValidationError {
        code
        type
        message
      }
      ... on ResponseIntegrityError {
        code
        type
        message
      }
      ... on ResponseInternalError {
        code
        type
        message
      }
    }
  }
}
`;

get_zones_query = (cityId) => {
  return `query select2Queries {
    select2 {
      zones (cityId: ${cityId}){
        id
        text
        __typename
      }
    }
  }`;
};

initSelect2 = (obj, multiple = true) => {
  $(obj.html_id).select2({
    width: "100%",
    allowClear: true,
    placeholder: "Seleccione una opción",
    minimumResultsForSearch: -1,
    multiple: multiple,
    ajax: {
      url: Django.graphql_url,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ query: obj.query }),
      processResults: function (response) {
        // Transforms the top-level key of the response object from 'items' to 'results'
        return {
          results: response.data.select2[obj.attr],
        };
      },
      // Additional AJAX parameters go here; see the end of this chapter for the full code of this example
    },
  });
};

initSelect2Multiple = () => {
  var listado = [
    { html_id: "#specializations", query: specializationsQuery, attr: "specializations" },
    { html_id: "#languages", query: languageQuery, attr: "languages" },
  ];

  for (i = 0; i < listado.length; i++) {
    initSelect2(listado[i]);
  }
};

initSelect2Basic = () => {
  var listado = [
    { html_id: "#carreer", query: carrersQuery, attr: "carreers" },
    // { html_id: "#city", query: citiesQuery, attr: "cities" },
  ];

  for (i = 0; i < listado.length; i++) {
    initSelect2(listado[i], false);
  }
};

initSelect2Basic();

initSelect2Multiple();

$("#city")
  .select2({
    width: "100%",
    allowClear: true,
    placeholder: "Seleccione una opción",
    minimumResultsForSearch: -1,
    multiple: false,
    ajax: {
      url: Django.graphql_url,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ query: citiesQuery }),
      processResults: function (response) {
        // Transforms the top-level key of the response object from 'items' to 'results'
        return {
          results: response.data.select2.cities,
        };
      },
      // Additional AJAX parameters go here; see the end of this chapter for the full code of this example
    },
  })
  .on("change", function () {
    $cityId = this.value;
    if ($cityId != null) {
      $("#zone").select2({
        width: "100%",
        allowClear: true,
        placeholder: "Seleccione una opción",
        minimumResultsForSearch: -1,
        multiple: true,
        ajax: {
          url: Django.graphql_url,
          method: "POST",
          contentType: "application/json",
          data: JSON.stringify({ query: get_zones_query($cityId) }),
          processResults: function (response) {
            // Transforms the top-level key of the response object from 'items' to 'results'
            return {
              results: response.data.select2.zones,
            };
          },
          // Additional AJAX parameters go here; see the end of this chapter for the full code of this example
        },
      });
    }
    return false;
  });

registerUser = (attachmentIds = []) => {
  // console.log({
  //   input: {
  //     genderEnum: $("#gender").val(),
  //     serviceMethodEnum: $("#service_method").val(),
  //     serviceModalityEnum: $("#service_modality").val(),
  //     password: $("#password").val(),
  //     passwordConfirm: $("#password_confirm").val(),
  //     email: $("#email").val(),
  //     username: $("#username").val(),
  //     firstName: $("#first_name").val(),
  //     lastName: $("#last_name").val(),
  //     nroDni: $("#nro_dni").val(),
  //     nroMatricula: $("#nro_matricula").val(),
  //     cuit: $("#cuit").val(),
  //     phone: $("#phone").val(),
  //     facebookProfile: $("#facebook").val() || null,
  //     instagramProfile: $("#instagram").val() || null,
  //     linkedinProfile: $("#linkedin").val() || null,
  //     attachmentIds: attachmentIds,
  //     experienceSummary: $("#experience_summary").val(),
  //     specializations: $("#specializations").val(),
  //     languages: $("#languages").val(),
  //     carreer: $("#carreer").val().toString(),
  //     officeLocations: $("#zone").val(),
  //   },
  // });

  $.ajax({
    url: Django.graphql_url,
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      query: newUserMutation,
      variables: {
        input: {
          genderEnum: $("#gender").val(),
          serviceMethodEnum: $("#service_method").val(),
          serviceModalityEnum: $("#service_modality").val(),
          password: $("#password").val(),
          passwordConfirm: $("#password_confirm").val(),
          email: $("#email").val(),
          username: $("#username").val(),
          firstName: $("#first_name").val(),
          lastName: $("#last_name").val(),
          nroDni: $("#nro_dni").val(),
          nroMatricula: $("#nro_matricula").val(),
          cuit: $("#cuit").val(),
          phone: $("#phone").val(),
          facebookProfile: $("#facebook").val() || null,
          instagramProfile: $("#instagram").val() || null,
          linkedinProfile: $("#linkedin").val() || null,
          attachmentIds: attachmentIds,
          experienceSummary: $("#experience_summary").val(),
          specializations: $("#specializations").val(),
          languages: $("#languages").val(),
          carreer: $("#carreer").val().toString(),
          officeLocations: $("#zone").val(),
        },
      },
    }),
    success: function (response) {
      notification = new deciresAlert();
      if (
        response.data &&
        response.data.psychology &&
        response.data.psychology.newProfessional &&
        response.data.psychology.newProfessional.originalId
      ) {
        notification.basic("Éxito", "Se ha registrado exitosamente en la plataforma", "success");
      } else {
        console.error(response.data.psychology.newProfessional);
        notification.basic(
          "Ups, algo salió mal!",
          "No hemos podido registrarte en la plataforma",
          "warning"
        );
      }

      setTimeout(function () {
        location.href = Django.urls.home;
      }, 9000);
    },
    error: function (error) {
      // Manejar errores
      console.error(error);
      notification.basic(
        "Ups, algo salió mal!",
        "No hemos podido registrarte en la plataforma, contacta al administrador del sistema.",
        "error"
      );
    },
  });
  return 0;
};

uploadAttachment = (html_id = "avatar") => {
  var fileInput = document.getElementById(html_id);
  var file = fileInput.files[0];
  var formData = new FormData();
  formData.append("attachment", file);
  formData.append("source_type", 1);
  formData.append("description", "ImageProfile");
  $.ajax({
    url: Django.urls.uploadAttachment,
    method: "POST",
    contentType: false,
    processData: false,
    data: formData,
    success: function (response) {
      console.log("Éxito:", response);
      if (response.originalId) {
        originalId = response.originalId.toString();
        registerUser([originalId]);
      }
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
  return 0;
};
