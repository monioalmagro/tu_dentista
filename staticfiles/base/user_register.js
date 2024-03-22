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
        membershipPlanEnum
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

const getMembershipPlans = `
  query getMembershipPlans{
    psychology{
      getMembershipPlans{
        originalId
        membership
        price
        membershipOptions
        __typename
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
          personalAddress: $("#personal_address").val(),
          membershipPlanEnum: $("#membership_plan").val(),
          attentionSchedule: $("#attention_schedule").val(),
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
        setTimeout(function () {
          location.href = Django.urls.home;
        }, 5000);
      } else {
        console.error(response);
        notification.basic(
          "Ups, algo salió mal!",
          "No hemos podido registrarte en la plataforma",
          "warning"
        );
      }
      return false;
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

uploadAttachment = () => {
  var avatarInput = document.getElementById("avatar");
  var avatarFile = avatarInput.files[0];

  var dniInput = document.getElementById("dni");
  var dniFile = dniInput.files[0];

  var matriculaInput = document.getElementById("matricula");
  var matriculaFile = matriculaInput.files[0];

  var formData = new FormData();

  formData.append("avatar", avatarFile);
  formData.append("avatar_data", JSON.stringify({ source_type: 1, description: "User AVATAR" }));

  formData.append("dni", dniFile);
  formData.append("dni_data", JSON.stringify({ source_type: 2, description: "User DNI" }));

  formData.append("matricula", matriculaFile);
  formData.append(
    "matricula_data",
    JSON.stringify({ source_type: 3, description: "User MATRICULA" })
  );

  $.ajax({
    url: Django.urls.uploadAttachment,
    method: "POST",
    contentType: false,
    processData: false,
    data: formData,
    success: function (response) {
      if (response.originalIds) {
        registerUser(response.originalIds);
      }
    },
    error: function (error) {
      console.error("Error:", error);
    },
  });
  return 0;
};

/* ## MEMBERSHIP PLAN ## */

membershipPlanSection = (obj, index) => {
  features = ``;
  features_data = obj.membershipOptions.items;
  btn_id = null;

  if (index == 0) {
    btn_id = "membership_basic";
    for (i = 0; i < features_data.length; i++) {
      if (features_data[i] == features_data[0]) {
        features += `<li>${features_data[i]}</li>`;
      } else {
        features += `<li><del>${features_data[i]}</del></li>`;
      }
    }
  } else {
    btn_id = "membership_premium";
    for (k = 0; k < features_data.length; k++) {
      features += `<li>${features_data[k]}</li>`;
    }
  }

  return `<li data-animation="true" data-animation-type="fadeInUp">
            <div class="pricing-container bg-white">
              <h3 class="bg-orange text-dark">${obj.membership}</h3>
              <div class="price bg-orange">
                <div class="price-figure">
                  <span class="price-number  text-dark">$${obj.price}</span>
                  <span class="price-tenure">${obj.membershipOptions.modalidad}</span>
                </div>
              </div>
              <ul class="features">
                ${features}
              </ul>
              <div class="footer bg-white" >
                <a class="btn btn-warning text-dark" id="${btn_id}">
                  Seleccionar
                </a>
              </div>
            </div>
          </li>`;
};

$.ajax({
  url: Django.graphql_url,
  method: "POST",
  contentType: "application/json",
  data: JSON.stringify({
    query: getMembershipPlans,
    variables: {},
  }),
  success: function (response) {
    $data = response.data.psychology.getMembershipPlans;

    $html = `<li data-animation="true" data-animation-type="fadeInUp"></li>`;
    for (j = 0; j < $data.length; j++) {
      $html += membershipPlanSection($data[j], j);
    }

    $html += `<li data-animation="true" data-animation-type="fadeInUp"></li>`;
    $("#features").empty().append($html);

    //  BTN FUNCTIONS

    $("#membership_basic").on("click", function (e) {
      e.preventDefault();
      $btn_selected = $(this).addClass("btn-dark text-white").removeClass("btn-warning text-dark");
      $("#membership_premium").addClass("btn-warning text-dark").removeClass("btn-dark text-white");
      $("#membership_plan").val("BASICO");
    });

    $("#membership_premium").on("click", function (e) {
      e.preventDefault();
      $btn_selected = $(this).addClass("btn-dark text-white").removeClass("btn-warning text-dark");
      $("#membership_basic").addClass("btn-warning text-dark").removeClass("btn-dark text-white");
      $("#membership_plan").val("PREMIUM");
    });

    return false;
  },
  error: function (error) {
    // Manejar errores
    console.error(error);
  },
});

/* ## MEMBERSHIP PLAN ## */
